# What ADS-B Is

Outcome: by the end of this chapter you
can say what an aircraft broadcasts, how
often, and why a stranger with a cheap
radio is allowed — intended, even — to
hear it.

For most of aviation history, knowing
where an aircraft was required radar:
a ground station sent out a pulse, and
timed the echo. The aircraft was passive.
**ADS-B** turns that around. The name
unpacks to **Automatic Dependent
Surveillance — Broadcast**, and each
word earns its place:

- **Automatic** — no pilot action and no
  ground station asking. The
  **transponder** (the radio box that
  answers radar) sends the broadcasts on
  its own, roughly twice a second for
  position.
- **Dependent** — the aircraft reports
  what its own navigation systems believe:
  position from satellite navigation,
  altitude from its pressure altimeter.
  It is a claim by the aircraft, not a
  measurement by the ground. Chapter 14
  returns to what that means for trust.
- **Surveillance** — the purpose: letting
  controllers, other aircraft and — as
  it turns out — anyone else keep track
  of who is where.
- **Broadcast** — one transmission,
  addressed to nobody, receivable by
  everybody in range.

A full broadcast set from one aircraft
tells you:

- its permanent **ICAO address**, a
  24-bit number unique to that airframe,
  written as six hex digits;
- its **callsign** (the flight number or
  registration it is flying under, like
  a name tag it can change per flight);
- its **position** — latitude and
  longitude, to a precision of a few
  metres;
- its **barometric altitude**, in feet;
- its **velocity** — ground speed,
  heading, and climb or descent rate;
- and housekeeping: how much to trust
  each value, whether an alert is set,
  and more.

Two flavours exist. **ADS-B Out** is the
broadcast itself — the half this guide
receives. **ADS-B In** is an aircraft
receiving *other* aircraft's broadcasts
for its own cockpit displays. Only Out
matters here, and in much of the world's
busy airspace Out is now mandatory
equipment, which is why the sky is so
thoroughly labelled.

The broadcasts ride on **1090 MHz**, the
same frequency Mode S transponders have
always used to answer radar
interrogations. An extended broadcast
packet — a **squitter**, in the trade's
unembarrassed vocabulary — is 112 bits
long and takes 120 microseconds to send.
Chapter 3 takes one apart.

Here is the property that makes this a
hobby at all: **the broadcasts are not
encrypted, and that is deliberate.** A
safety system that only authorised
receivers could hear would fail at its
job. Air traffic control hears them, but
so does a twenty-five-dollar television
dongle retuned to the frequency — see
the [RTL-SDR guide](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/)
in this series — and so do the volunteer
networks whose combined feeds draw the
live flight maps. Nothing in this guide
involves defeating any protection,
because there is none to defeat.

There is, though, a real decision hiding
in the hobby, and this guide will not
bury it. Receiving is passive and harms
nobody. *Redistributing* — feeding your
receiver's stream to a public network —
publishes two things: the traffic over
your neighbourhood, and the fact and
rough location of your receiver. Most
feeders are glad to do both; the
networks exist because they do. But it
is a choice, and chapter 11
(**Feeding, MLAT and Privacy**) walks
through it properly, including the
programmes that let some aircraft ask
not to be tracked publicly.

A last word about this guide's own
evidence, because it shapes everything
after chapter 3. The lab behind the
guide had no radio receiver, so it never
heard a real aircraft. Instead it
generated genuine packets for two
invented aircraft and fed them to the
real decoder — the same packets a real
transponder would send, arriving by
wire instead of by air. What that proves
(decoding, tracking, output) is claimed
fully. What it cannot prove (reception,
range, antennas) is taught from the
project's documentation and labelled.
Chapter 5 shows the whole trick, and
`criteria.md` keeps the ledger.
