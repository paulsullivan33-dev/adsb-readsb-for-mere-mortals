# Feeding, MLAT and Privacy

Outcome: you can say what feeding a
network gives and costs, explain how
multilateration finds aircraft that
never report a position, and make the
sharing decision with your eyes open.

This chapter is documented-only in its
mechanics — the lab fed nobody — but
its subject is a decision, and decisions
do not need a lab.

## What feeding is

The public flight maps — FlightAware,
ADS-B Exchange, Flightradar24,
airplanes.live, adsb.lol and others —
are mosaics of volunteer receivers. To
**feed** one is to run a small program
beside your decoder that forwards your
Beast output stream (chapter 8) to the
network, continuously. In return you
typically get an account upgrade on that
service, the pleasure of seeing your
coverage on the big map, and one
technical prize: MLAT.

Each network runs its own feeder
software and its own terms; several can
be fed at once from the same decoder,
which is why "which network?" is not an
either/or question. What they share is
the shape of the bargain: your data,
their map.

## MLAT: positions from timing

Some aircraft — older airliners, much
military and business traffic — carry
Mode S transponders that answer
interrogations but never broadcast a
position. No squitter, no coordinates:
chapter 3's messages simply do not
exist for them. **Multilateration**
fills the gap with geometry. If four or
more receivers hear the *same* reply and
report *exactly when* it arrived,
the differences in arrival times define
the sender's position — the same trick
as CPR, played by the network with
clocks instead of grids.

Three consequences follow:

- MLAT is a **network effect**. Your
  lone receiver cannot do it; you get
  MLAT results *back* from a network
  only because others feed too, and the
  results flow to you because you feed.
- It demands **timing honesty**. The
  12 MHz timestamp inside every Beast
  frame (chapter 12) exists for this.
  This is also why MLAT from a
  software-only timestamp is approximate
  and from GPS-disciplined hardware is
  better.
- MLAT aircraft appear in your
  `aircraft.json` with positions the
  network computed and returned, marked
  as MLAT-sourced — the decoder treats
  them as second-class citizens, and so
  should your confidence.

## The privacy paragraph, plainly

ADS-B broadcasts are public by design,
and receiving them is unremarkable. But
three facts deserve daylight before you
feed:

1. **You are publishing your receiver.**
   A feed necessarily reveals that a
   receiver exists near a location;
   networks coarsen feeders' displayed
   positions to differing degrees, but
   "somewhere in this town" is the
   minimum truth you disclose.
2. **You are publishing your sky.** The
   traffic pattern over your home is
   data about your neighbourhood. Most
   people judge this harmless — the
   aircraft were broadcasting anyway —
   but the judgement is yours to make,
   not a default to drift into.
3. **Not every aircraft wants an
   audience, and the system knows it.**
   Privacy programmes exist (in the US,
   the LADD list and PIA addresses let
   operators limit public tracking), and
   aggregators differ — visibly — in how
   they treat military traffic and
   blocked aircraft. Feeding different
   networks is, among other things,
   choosing among those policies.

None of this argues against feeding;
the public maps are a genuine common
good built entirely of these small
contributions, and this guide's author
networks exist because people feed.
It argues against feeding *unthinkingly*
— and for remembering that **not
feeding is also a complete hobby.** A
station that only ever draws its own
map loses MLAT and the warm glow, and
keeps everything else in this guide.
