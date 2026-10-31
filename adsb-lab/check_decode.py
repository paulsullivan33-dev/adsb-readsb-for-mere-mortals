#!/usr/bin/env python3
"""check_decode.py -- prove the decoder gave back the track we sent.

Reads make_fixture.py's intended track and the aircraft.json that
readsb wrote while consuming the fixture feed, and compares them
field by field. Positions are allowed 0.001 degrees of slack (CPR
quantises a position to a grid cell; the real agreement is far
tighter), speeds 1.5 kt, tracks half a degree. Everything else
must match exactly.

Usage: python3 check_decode.py aircraft-final.json
"""

import json
import sys

sys.path.insert(0, ".")
import make_fixture as fx


def main(path):
    data = json.load(open(path))
    by_hex = {a["hex"]: a for a in data["aircraft"]}
    rows = fx.track()
    _, exp_lat, exp_lon, exp_alt, ew, ns, _ = rows[-1]
    import math
    exp_gs = math.hypot(ew, ns)
    exp_trk = (math.degrees(math.atan2(ew, ns)) + 360) % 360

    checks = []
    a1 = by_hex.get("abc123")
    checks.append(("aircraft 1 present (hex abc123)", a1 is not None))
    if a1:
        checks.append(("callsign FICT1", a1["flight"].strip() == "FICT1"))
        checks.append((f"altitude {a1['alt_baro']} == {exp_alt}",
                       a1["alt_baro"] == exp_alt))
        checks.append((f"lat {a1['lat']:.6f} ~ {exp_lat:.6f}",
                       abs(a1["lat"] - exp_lat) <= 0.001))
        checks.append((f"lon {a1['lon']:.6f} ~ {exp_lon:.6f}",
                       abs(a1["lon"] - exp_lon) <= 0.001))
        checks.append((f"ground speed {a1['gs']} ~ {exp_gs:.1f}",
                       abs(a1["gs"] - exp_gs) <= 1.5))
        checks.append((f"track {a1['track']} ~ {exp_trk:.1f}",
                       abs(a1["track"] - exp_trk) <= 0.5))

    a2 = by_hex.get("def456")
    checks.append(("aircraft 2 present (hex def456)", a2 is not None))
    if a2:
        checks.append(("callsign TEST2", a2["flight"].strip() == "TEST2"))
        checks.append((f"altitude {a2['alt_baro']} == {fx.A2_ALT}",
                       a2["alt_baro"] == fx.A2_ALT))
        checks.append((f"lat {a2['lat']:.6f} ~ {fx.A2_LAT:.6f}",
                       abs(a2["lat"] - fx.A2_LAT) <= 0.001))
        checks.append((f"lon {a2['lon']:.6f} ~ {fx.A2_LON:.6f}",
                       abs(a2["lon"] - fx.A2_LON) <= 0.001))
        checks.append(("no ground speed (none was sent)",
                       "gs" not in a2))

    ok = True
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
        ok = ok and passed
    print(f"\n{'ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED'} "
          f"({sum(1 for _, p in checks if p)}/{len(checks)})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "aircraft-final.json"))
