# Decoding It Yourself

Outcome: you can take one packet apart
with nothing but the layout from chapter
3, and you know the shape of the stream
that carries packets between programs.

You will probably never *need* to do
this — readsb exists — but one packet
decoded by hand turns the whole system
from magic into machinery, and the
packet below is real: it is the odd
position frame of the fixture's first
step, taken from the lab's log, where
readsb decoded it on the facing line.

## One packet, by hand

```
*8dabc123583785a223982e540813;
```

The asterisks-and-semicolon dress is the
**AVR** format of chapter 8. Inside are
14 bytes. Take them in order:

- `8d` — binary `10001 101`: downlink
  format **17**, capability 5. An
  extended squitter from a normal
  airborne transponder.
- `abc123` — the next three bytes are
  the ICAO address. (Invented, as
  always in this guide.)
- The seven message bytes follow:
  `58 37 85 a2 23 98 2e`. The first five
  bits of `0x58` are `01011` = **type
  code 11**, an airborne position.
- The **altitude** is the next 12 bits:
  `0x378`. Its bit worth 16 is set —
  that is the **Q bit**, meaning "count
  in 25 ft steps". Removing the Q bit
  leaves 440 steps; 440 × 25 − 1000 =
  **10,000 ft**. The decoder's line
  agrees: "Baro altitude: 10000 ft".
- After a time flag (0) comes the **CPR
  format bit: 1 — this is an odd frame.**
- The last 34 bits split into the two
  17-bit CPR fractions: latitude
  **53521**, longitude **104494**. And
  here is the chapter 3 lesson one last
  time: these numbers are *not* a
  position. They became one —
  (32.999997, −96.999973), readsb's
  printed result — only in combination
  with the even frame that preceded
  them, fractions (65536, 69177).
- The final three bytes, `54 08 13`, are
  the **parity**. The lab's generator
  computed them with the polynomial of
  chapter 3; readsb recomputed them on
  arrival and stamped the packet
  "CRC: 000000 … decode: ok" — remainder
  zero, packet intact.

Every field in that walk came from the
tables in chapter 3 and a hex reader.
That is the whole skill; the decoder
just does it 300 times a minute without
getting bored.

## The Beast stream, byte by byte

Between programs, packets travel in
**Beast** frames. The lab's fixture file
(`adsb-lab/fixture.beast`, 125 messages,
2,876 bytes) begins:

```
1a 33 000000000000 80 8dabc123101890d4c608206f43cb
1a 33 0000001b7740 80 8ddef456105054d4ca08203c95c8
```

- `1a` is the escape byte that starts
  every frame; `33` — the character
  "3" — says "a full-length Mode S frame
  follows". (Shorter frames exist, with
  other type bytes.)
- Six bytes of **timestamp**: a counter
  ticking at 12 MHz, the heartbeat MLAT
  (chapter 11) lives on. The fixture's
  clock starts at zero; a real receiver's
  never stops.
- One **signal-level byte** — the RSSI
  the decoder reports. The fixture
  writes a constant `0x80`; the radio
  writes the truth.
- The **14 packet bytes** themselves.
- Any literal `0x1a` inside the data is
  sent doubled — the escape rule — which
  the fixture's frames happen not to
  need and a busy sky's do.

Replay the file into a decoder listening
on a Beast input port and the fixture
flight flies again, timestamps and all:

```
nc 127.0.0.1 30004 < adsb-lab/fixture.beast
```

## When you want a library instead

**pyModeS** is the Python library the
research community decodes with: feed it
hex strings like the one above and it
returns the same fields this chapter
extracted by hand, plus velocity,
identification and the CPR mathematics
implemented once, carefully. This guide
mentions it as documentation, not as
lab work — the lab's own code was the
*generator*, `make_fixture.py`, which
had to know the formats in the opposite
direction and is the more instructive
read. Between the two directions —
writing packets in the lab, reading them
here — there is nothing left in a
squitter that anyone is keeping from
you.
