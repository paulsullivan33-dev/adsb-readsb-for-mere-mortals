# The Neighbours

Outcome: you can place readsb in its
family, name the thing you would run
instead for each neighbouring job, and
say what each does that readsb doesn't.

## The dump1090 family

Almost every ADS-B decoder on Earth is
one program wearing descendants:

- **dump1090 (antirez, 2012).** The
  original: a weekend proof that a TV
  dongle could decode transponders,
  grown into the reference
  implementation. Its credits line —
  printed in this fork's own `--help`,
  and quoted in chapter 4 — is the
  family tree.
- **Malcolm Robb's fork** added the
  interactive table and much polish.
- **dump1090-mutability** restructured
  the code for packaging and modern
  features; it became **dump1090-fa**,
  FlightAware's maintained version,
  shipped in the PiAware image. If you
  run PiAware, this is your decoder:
  solid, conservative, and configured
  the FlightAware way.
- **readsb (Mictronics)** forked the fa
  line to push performance and features
  — multithreading groundwork, better
  tracking, the globe work — and
  **wiedehopf's readsb** is its current
  centre of gravity: the fastest-moving
  fork, the one tar1090 is designed
  against, and the one this guide built.

The honest differences are of tempo and
extras, not of kind: all of them decode
the same packets to the same JSON shape,
which is why guides, tools and tar1090
move between them so freely.

## Ready-made stations

- **PiAware (FlightAware)** and its
  rivals' images — a whole feeder
  station on an SD card. The neighbour
  to choose when the goal is feeding,
  not understanding.
- **ADS-B Exchange and adsb.lol images**
  — the same idea from the
  community-aggregator side.

## Other receivers and decoders

- **OpenWebRX** — this series has a
  [guide](https://paulsullivan33-dev.github.io/openwebrx-for-mere-mortals/)
  for it: a general web SDR that hosts
  many modes in a browser. Its home
  ground is listening broadly; readsb's
  is this one job, done deeply.
- **Hardware receivers** — the original
  Mode-S Beast box (whose stream format
  this guide dissected), AirSquitter,
  Mode-S Beast-based and integrated
  units. They trade money for
  timestamps disciplined well enough to
  make MLAT sing, and for never needing
  a package update.
- **pyModeS** (chapter 12) — not a
  station but a scholar: a decoding
  library for research and for your own
  scripts, where readsb is a service.
- **The radar sites themselves** —
  FlightAware and kin are neighbours in
  the other direction: consumers of a
  hundred thousand stations like yours,
  returning MLAT and the global picture.

## Choosing, in one breath

Build **readsb** (this fork) if you want
the current tool and intend to
understand it; take **PiAware** if you
want to be feeding by lunch; keep a
**hardware receiver** if MLAT precision
is the point; reach for **pyModeS** when
the packets themselves are the research.
The packets do not care. They are the
same packets for everyone — that was
chapter 1's whole point.
