#!/usr/bin/env python3
"""make_fixture.py -- a tiny, honest ADS-B fixture generator.

Builds real Mode S DF17 "extended squitter" messages for two FICTIONAL
aircraft, wraps them in the Beast binary protocol, and either serves
them on a loopback TCP port (for readsb --net-connector beast_in) or
writes them to a .beast file.

Nothing here is a real aircraft. The ICAO addresses, callsigns and the
track itself were invented for this guide's lab. The message formats,
CRC and CPR position encoding are the real, published ones -- that is
the point: a real decoder (readsb) accepts these frames and decodes
them back to the track below, which is how the guide proves its claims.

Usage:
    python3 make_fixture.py serve [port]     # TCP server (default 18112)
    python3 make_fixture.py file  out.beast  # write the stream to a file
    python3 make_fixture.py track            # print the intended track
"""

import math
import socket
import sys
import time

# ---------------------------------------------------------------- CRC
# Mode S parity: 24-bit CRC, generator polynomial 0xFFF409 (x^24 + ...).
# For DF17 the parity is the plain CRC remainder of the first 11 bytes.

def crc24(data11: bytes) -> int:
    poly = 0x1FFF409  # degree-24 generator, top bit included
    reg = 0
    bits = []
    for byte in data11:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    bits.extend([0] * 24)  # augment with 24 zero bits
    for b in bits:
        reg = (reg << 1) | b
        if reg & (1 << 24):
            reg ^= poly
    return reg & 0xFFFFFF


def df17(icao: int, me: bytes) -> bytes:
    """Assemble a full 14-byte DF17 message from ICAO address + 7-byte ME."""
    assert len(me) == 7
    first = bytes([0x8D]) + icao.to_bytes(3, "big")  # DF17, CA=5
    body = first + me
    return body + crc24(body).to_bytes(3, "big")


# ---------------------------------------------------------------- CPR
# Compact Position Reporting: a position is sent as two frames, "even"
# and "odd", each carrying 17-bit fractions of latitude and longitude
# inside a grid cell. The decoder combines a pair to get the position.

def _nl(lat: float) -> int:
    """Number of longitude zones at this latitude (standard formula)."""
    if lat == 0:
        return 59
    if abs(lat) == 87:
        return 2
    if abs(lat) > 87:
        return 1
    nz = 15
    x = 1 - (1 - math.cos(math.pi / (2 * nz))) / (math.cos(math.radians(lat)) ** 2)
    return int(math.floor(2 * math.pi / math.acos(x)))


def cpr_encode(lat: float, lon: float, odd: bool):
    dlat = 360.0 / (59 if odd else 60)
    yz = int(math.floor(131072 * ((lat % dlat) / dlat) + 0.5)) % 131072
    nl = _nl(lat)
    dlon = 360.0 / max(nl - (1 if odd else 0), 1)
    xz = int(math.floor(131072 * ((lon % dlon) / dlon) + 0.5)) % 131072
    return yz, xz


# ---------------------------------------------------------------- ME builders

def _pack(bits) -> bytes:
    """Pack a list of (value, width) pairs into bytes, MSB first."""
    acc = 0
    total = 0
    for value, width in bits:
        acc = (acc << width) | (value & ((1 << width) - 1))
        total += width
    assert total % 8 == 0
    return acc.to_bytes(total // 8, "big")


def me_ident(callsign: str, tc: int = 2) -> bytes:
    """TC 1-4: aircraft identification. Callsign is 8 chars, 6 bits each."""
    table = {" ": 32}
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        table[ch] = i + 1
    for i, ch in enumerate("0123456789"):
        table[ch] = 48 + i
    cs = (callsign + " " * 8)[:8]
    bits = [(tc, 5), (0, 3)]  # type code, category 0
    for ch in cs:
        bits.append((table[ch], 6))
    return _pack(bits)


def _alt_field(feet: int) -> int:
    """12-bit barometric altitude field, Q bit set (25 ft steps)."""
    v = int((feet + 1000) / 25)  # 11-bit value
    return ((v & 0x7F0) << 1) | 0x10 | (v & 0x00F)


def me_position(lat, lon, alt_ft, odd: bool, tc: int = 11) -> bytes:
    """TC 9-18: airborne position, barometric altitude."""
    yz, xz = cpr_encode(lat, lon, odd)
    return _pack([
        (tc, 5),
        (0, 2),            # surveillance status: no condition
        (0, 1),            # single-antenna flag
        (_alt_field(alt_ft), 12),
        (0, 1),            # time flag
        (1 if odd else 0, 1),
        (yz, 17),
        (xz, 17),
    ])


def me_velocity(ew_kt: int, ns_kt: int, vr_fpm: int) -> bytes:
    """TC 19 subtype 1: ground speed from east/west + north/south parts."""
    def comp(c):
        return (1 if c < 0 else 0), (abs(c) + 1 if c != 0 else 0)
    ew_sign, ew_val = comp(ew_kt)
    ns_sign, ns_val = comp(ns_kt)
    vr_sign = 1 if vr_fpm < 0 else 0
    vr_val = abs(vr_fpm) // 64 + 1
    return _pack([
        (19, 5), (1, 3),   # type code, subtype 1
        (0, 1),            # intent change
        (0, 1),            # reserved
        (0, 3),            # navigation accuracy category for velocity
        (ew_sign, 1), (ew_val, 10),
        (ns_sign, 1), (ns_val, 10),
        (0, 1),            # vertical rate source: barometric
        (vr_sign, 1), (vr_val, 9),
        (0, 2),            # reserved
        (0, 1), (0, 7),    # altitude difference sign + value (unused)
    ])


# ---------------------------------------------------------------- the track
# Aircraft 1 flies an invented two-leg track. Each step is 5 seconds of
# flight. Leg 1: heading 045, 400 kt, climbing. Leg 2: heading ~094,
# 399 kt, level. Aircraft 2 sits at one spot broadcasting its position.

STEPS = 24
DT = 5.0  # seconds of flight per step

A1_ICAO = 0xABC123
A1_CALL = "FICT1"
A2_ICAO = 0xDEF456
A2_CALL = "TEST2"
A2_LAT, A2_LON, A2_ALT = 33.1000, -96.9000, 0


def track():
    lat, lon = 33.0000, -97.0000
    rows = []
    for step in range(STEPS):
        if step < 12:
            ew, ns, vr = 283, 283, (512 if step < 6 else 0)
        else:
            ew, ns, vr = 398, -28, 0
        alt = 10000 + 25 * min(step, 8)
        rows.append((step, lat, lon, alt, ew, ns, vr))
        lat += ns * (DT / 3600.0) / 60.0
        lon += ew * (DT / 3600.0) / (60.0 * math.cos(math.radians(lat)))
    return rows


def message_stream():
    """Yield (delay_seconds, df17_bytes) for the whole fixture, looping
    the final state at the end so a late snapshot still sees it."""
    rows = track()
    # identification first, twice each
    for _ in range(2):
        yield 0.05, df17(A1_ICAO, me_ident(A1_CALL))
        yield 0.05, df17(A2_ICAO, me_ident(A2_CALL))
    for (step, lat, lon, alt, ew, ns, vr) in rows:
        yield 0.12, df17(A1_ICAO, me_position(lat, lon, alt, odd=False))
        yield 0.02, df17(A1_ICAO, me_velocity(ew, ns, vr))
        yield 0.02, df17(A1_ICAO, me_position(lat, lon, alt, odd=True))
        yield 0.02, df17(A2_ICAO, me_position(A2_LAT, A2_LON, A2_ALT, odd=False))
        yield 0.02, df17(A2_ICAO, me_position(A2_LAT, A2_LON, A2_ALT, odd=True))
    # tail: keep re-sending the final state
    step, lat, lon, alt, ew, ns, vr = rows[-1]
    while True:
        yield 1.0, df17(A1_ICAO, me_position(lat, lon, alt, odd=False))
        yield 0.05, df17(A1_ICAO, me_position(lat, lon, alt, odd=True))
        yield 0.05, df17(A1_ICAO, me_velocity(ew, ns, vr))
        yield 0.05, df17(A2_ICAO, me_position(A2_LAT, A2_LON, A2_ALT, odd=False))
        yield 0.05, df17(A2_ICAO, me_position(A2_LAT, A2_LON, A2_ALT, odd=True))


# ---------------------------------------------------------------- Beast

def beast_frame(msg: bytes, tick: int) -> bytes:
    out = bytearray(b"\x1a\x33")  # escape, '3' = DF17-length frame
    out += (tick & 0xFFFFFFFFFFFF).to_bytes(6, "big")  # 12 MHz timestamp
    out += bytes([0x80])  # signal level byte (arbitrary in a fixture)
    for b in msg:
        out.append(b)
        if b == 0x1A:
            out.append(0x1A)  # escape literal 0x1a bytes
    return bytes(out)


def serve(port: int):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(1)
    print(f"fixture server listening on 127.0.0.1:{port}", flush=True)
    conn, addr = srv.accept()
    print(f"client connected from {addr}", flush=True)
    tick = 0
    try:
        for delay, msg in message_stream():
            time.sleep(delay)
            tick += 1_800_000  # 0.15 s of the 12 MHz Beast clock per step
            conn.sendall(beast_frame(msg, tick))
    except (BrokenPipeError, ConnectionResetError):
        print("client disconnected", flush=True)
    finally:
        conn.close()
        srv.close()


def write_file(path: str):
    """Write one full pass of the fixture (no infinite tail) to a file."""
    gen = message_stream()
    tick = 0
    n = 0
    with open(path, "wb") as fh:
        for delay, msg in gen:
            fh.write(beast_frame(msg, tick))
            tick += 1800000
            n += 1
            if n > 4 + STEPS * 5:  # prelude + all steps, skip the tail
                break
    print(f"wrote {n} messages to {path}")


def print_track():
    print("Intended track for aircraft 1 "
          f"(ICAO {A1_ICAO:06x}, callsign {A1_CALL}):")
    print("step      lat       lon  alt_ft  ew_kt  ns_kt  vr_fpm   gs_kt  track")
    for (step, lat, lon, alt, ew, ns, vr) in track():
        gs = math.hypot(ew, ns)
        trk = (math.degrees(math.atan2(ew, ns)) + 360) % 360
        print(f"{step:4d}  {lat:8.4f} {lon:9.4f}  {alt:6d}  {ew:5d}  {ns:5d}"
              f"  {vr:6d}  {gs:6.1f}  {trk:5.1f}")
    print(f"\nAircraft 2 (ICAO {A2_ICAO:06x}, callsign {A2_CALL}): static at "
          f"lat {A2_LAT:.4f}, lon {A2_LON:.4f}, alt {A2_ALT} ft, no velocity.")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "track"
    if mode == "serve":
        serve(int(sys.argv[2]) if len(sys.argv) > 2 else 18112)
    elif mode == "file":
        write_file(sys.argv[2])
    else:
        print_track()
