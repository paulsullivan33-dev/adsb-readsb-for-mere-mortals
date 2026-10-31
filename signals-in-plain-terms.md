# The Signals in Plain Terms

Outcome: you can sketch a Mode S packet,
name the four message kinds that carry
almost everything, and explain — with
the decoder's own words — why a position
needs two frames, not one.

## The packet

A Mode S transmission is **112 bits**,
sent by pulse-position modulation: a
pulse in the first half of a microsecond
means 1, in the second half means 0. A
**preamble** of four pulses in a fixed
pattern announces "packet starting", and
a decoder like readsb spends most of its
life scanning samples for that pattern.

The 112 bits divide into four fields:

| Bits | Field | Holds |
|---|---|---|
| 5 | **DF** | the *downlink format* — what kind of packet this is |
| 3 | capability | the transponder's class |
| 24 | **ICAO address** | which aircraft (or, in replies, part of the check) |
| 56 | **ME** | the message itself, for extended squitters |
| 24 | **parity** | an error check computed over everything before it |

**DF 17** is the format this guide lives
on: the *extended squitter*, the
unsolicited broadcast ADS-B is made of.
(DF 11 is the shorter "all-call" reply a
transponder gives when radar or a ground
station asks who is out there; DF 0, 4,
5, 20 and 21 are answers to specific
interrogations. A busy decoder sees all
of them; the broadcasts are the ones
carrying positions.)

## The parity check earns its keep

The last 24 bits are a **CRC** — a
checksum computed from the other 88 bits
by a published polynomial. The decoder
recomputes it for every packet; a
mismatch means radio noise mangled the
bits, and the packet is discarded. This
is not decoration. In this guide's own
lab, readsb's final statistics read:

```
369 Mode S messages received
    0 with bad message format or invalid CRC
  369 accepted with correct CRC
```

— the fixture generator had to get its
CRC arithmetic exactly right before the
decoder would accept a single invented
packet, which is the surest sign the
generator was producing the real thing.

## Inside the ME field: type codes

The first five bits of the 56-bit
message are a **type code** (TC) that
says what the rest means:

- **TC 1–4 — identification.** The
  callsign, eight characters, packed six
  bits at a time. ("FICT1" and "TEST2"
  in the lab.)
- **TC 9–18 — airborne position.**
  Barometric altitude, plus latitude and
  longitude in CPR encoding (below).
- **TC 19 — airborne velocity.** Ground
  speed sent as separate east-west and
  north-south components, plus climb or
  descent rate. The decoder combines the
  components into the speed and track
  (heading) you see on maps.
- **TC 20–22 — position with GNSS
  height**: the same idea with satellite
  altitude instead of pressure altitude.
- **TC 28, 29, 31** — status and
  operational messages: emergencies,
  resolution advisories, capability
  reports. Real, but not needed to draw
  a map.

Altitude in a position message is a
count of 25-foot steps above −1000 ft,
which is why decoded altitudes are
always multiples of 25. Velocity
components are in knots, offset by one —
a quirk that matters in chapter 12 when
a packet is read by hand.

## CPR: the two-frame position

Here is the one genuinely clever idea in
the whole system. A position message
does **not** contain a latitude and
longitude. It contains two 17-bit
fractions that locate the aircraft
inside a grid cell — but not which cell.
This is **Compact Position Reporting**
(CPR), and a single frame is deliberately
ambiguous: the same fractions repeat in
cells all over the globe.

The resolution is the **even/odd pair**.
Frames alternate between two slightly
different grids, marked by a flag bit.
An even frame and an odd frame received
close together (within about ten
seconds) disagree about the grid in a
way that identifies exactly one cell on
Earth, and the position falls out
precisely. This is called **global
decoding**, and the decoder needs both
halves — which this guide's lab watched
happen in the decoder's own log. The
first position frame of the fixture
flight produced:

```
CPR decoding:  none
```

and its twin, a fraction of a second
later:

```
CPR latitude:    32.999997 (53521)
CPR longitude:  -96.999973 (104494)
CPR decoding:  global
```

There is also **local decoding**: one
frame plus a known reference position
(your receiver's own location, or the
aircraft's last known position) can pin
the cell when it lies within about
180 nautical miles. It is why readsb
asks for your `--lat` and `--lon` — and
why a wrong receiver location quietly
breaks position decoding near the edges.
Chapter 15 has that story.

The statistics keep score of all this.
The lab's run ended with **291 airborne
position messages** and **289 global CPR
attempts with valid positions** — the
pairs that found each other. The two
that did not were the harmless first
frames of each aircraft, which arrived
before any partner existed.

Squitter rates make the pairing easy in
practice: position frames alternate even
and odd, each about twice a second, so a
decoder in radio range usually holds a
fresh global position for every aircraft
within half a second of first hearing
it. The fixture sent its pairs back to
back, which is slightly tidier than
reality but changes nothing about the
arithmetic.
