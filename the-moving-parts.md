# The Moving Parts

Outcome: you can name the five parts of
a receiving station, say which part
holds the knowledge at each step, and
place readsb in the chain — including
the ways of feeding it that involve no
radio at all.

A receiving station is a chain, and most
confusion in this hobby comes from
blaming the wrong link. Here is the
whole chain, in the order a packet
travels:

**1. The antenna.** A passive piece of
metal sized for 1090 MHz — the
wavelength is about 27.5 cm, so a simple
quarter-wave element is under 7 cm long.
It converts the broadcast into a faint
electrical signal. It knows nothing; a
bad position or a long, lossy cable can
starve everything downstream while every
program looks healthy. Chapter 10 is
devoted to it.

**2. The radio dongle.** Almost always a
USB **software-defined radio** — an
RTL-SDR stick or a relative. It tunes to
1090 MHz and digitises a slice of radio
spectrum several million times a second,
handing the computer a stream of raw
samples. It still knows nothing: the
samples are just numbers describing a
waveform. Its one judgement call is
**gain** — how much to amplify — and
chapter 10 explains why that call is
delicate.

**3. The decoder — readsb.** This is
where numbers become aircraft. readsb
watches the sample stream for the
distinctive pulse pattern of a Mode S
packet, demodulates the bits, checks
each packet's error code, decodes the
message types, solves positions from
paired frames (chapter 3), and keeps a
running table: every aircraft heard
from, its last position, speed, altitude
and how long ago it was last seen.
Entries fade out when an aircraft goes
silent — the table is a *state*, not a
recording. Everything before this point
is radio; everything after it is data.

**4. The outputs.** readsb republishes
what it knows, several ways at once: as
**files** (`aircraft.json` and friends,
rewritten every second), and as
**network streams** in the formats other
programs expect — Beast (compact binary,
the lingua franca between receivers),
raw text, and the older SBS format.
Chapter 8 tours them. This is also where
other people's readsb instances connect:
a decoder can consume another decoder's
Beast stream instead of a radio, which
is precisely the door this guide's lab
walks through in chapter 5, and how
stations merge coverage in chapter 12.

**5. The display and the feeders.** A
map program — usually **tar1090**,
chapter 9 — reads the JSON and draws
aircraft on a map in your browser.
Separately, small feeder programs offer
your Beast stream to the public
aggregator networks. The decoder itself
neither draws nor phones home; those
are neighbours, not parts of readsb.

Two consequences of this layout are
worth keeping. First, **the decoder is
testable without the radio.** Because
part 3 consumes a stream, any honest
stream will do — including a generated
one. A station that decodes the fixture
in chapter 5 correctly has a proven
decoder, and any later failure with a
real antenna belongs to parts 1–2.
Second, **the state is disposable.** If
readsb restarts, its table empties and
refills within seconds as broadcasts
arrive. Nothing precious lives in the
decoder; the precious things are the
antenna's placement and the archive of
JSON, if you keep one.

The one part that is *not* in the chain:
a transmitter. A receiving station never
transmits anything on 1090 MHz — the
dongle cannot, and the decoder has no
reason to. Your station is a listener,
which is both its legal comfort and its
limitation: it can only work with what
aircraft choose to announce.
