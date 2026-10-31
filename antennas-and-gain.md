# Antennas, Gain and Range

Outcome: you can predict, before buying
anything, roughly what a station will
hear — and diagnose the two ways a
station deafens itself.

This chapter is **documented-only**: the
lab had no antenna to raise. It is
grounded in the readsb documentation
and the radio principles covered by this
series' [RTL-SDR guide](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/),
and it contains no measurement of the
lab's own, because there was nothing to
measure with.

## The physics that decides everything

1090 MHz signals travel in straight
lines and are blocked by terrain,
buildings and the curve of the Earth.
The range of a station is therefore set
by the **radio horizon**: an aircraft at
35,000 ft can be "seen" from roughly
200 nautical miles away by a receiver at
sea level, and every metre of antenna
height adds a little more. Two
consequences dominate the hobby:

- **Height beats everything.** Moving an
  antenna from a desk to a roof commonly
  doubles the traffic. No amplifier,
  filter or decoder setting does that.
- **Low aircraft are local aircraft.**
  Something on final approach at
  1,500 ft may only be visible for
  30–40 miles. A map that shows
  airliners at 200 miles and nothing at
  the nearby airfield is not broken;
  it is geometry.

Expect, for a decent rooftop station,
150–250 nautical miles on high traffic
and a message rate from a few dozen to
a few thousand per minute depending on
how busy your sky is. The lab's fixture
rate (369 messages in 69 seconds from
two pretend aircraft) is, by design,
not evidence about any of this.

## The antenna itself

The wavelength at 1090 MHz is about
27.5 cm, so antennas are small:

- A **quarter-wave ground plane** —
  a 6.9 cm vertical element over a few
  radial wires — is a legitimate antenna
  you can build in minutes, and the
  plans in the RTL-SDR community are
  measured in soft-drink cans.
- The **telescopic whip** bundled with
  dongles works, poorly, at a length
  that happens to suit some other band.
- **Dedicated 1090 MHz antennas**
  (collinear designs in a fibreglass
  tube) are the standard purchase: modest
  gain in all directions, weatherproof,
  made for exactly this frequency.
- **Cable is a cost, not a conduit.** At
  1090 MHz, cheap coax can eat most of
  your signal in a long run. The standard
  solution is counterintuitive and
  correct: put the *dongle and computer
  at the antenna* (a small board on the
  mast or in the attic) and let the
  network cable be the long run instead.

## Gain: the delicate knob

The dongle's amplifier must lift a
whisper without shouting over itself.
Too little gain and distant aircraft
stay under the noise. Too much and the
strong signal of a nearby aircraft
**overloads** the receiver — samples
clip, and paradoxically the decoder
sees *fewer* aircraft as gain rises,
because the loud traffic tramples the
quiet. On a map this looks like being
deaf in a busy sky.

readsb's **autogain** (the default for
RTL-SDR in this fork, per its README)
exists precisely because the right
setting is local and time-varying. The
honest way to judge your own setting,
documented in the project's materials,
is in `stats.json`: the distribution of
received signal strengths, and
specifically the share of messages
arriving near full scale. A healthy
station has strong signals that stop
short of the ceiling.

Two accessories sit between antenna and
dongle on many stations, both treating
real diseases: a **band-pass filter**
for 1090 MHz, where strong out-of-band
signals (mobile phone masts are the
usual suspect) overload the front end
even at sane gain; and an **LNA** (a
low-noise amplifier at the antenna) for
long cable runs, which amplifies before
the cable can subtract. Neither fixes a
bad location, and both are cheaper than
regret in the wrong order: antenna
position first, then gain, then
accessories.

## The one honest summary

Range claims in this hobby are usually
true and usually useless, because they
describe somebody else's roof. Your
station's truth is in its own statistics
after a week of running — which is why
chapter 6 insisted statistics are a
habit, not a garnish.
