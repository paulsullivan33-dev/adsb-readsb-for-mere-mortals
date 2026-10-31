# ADS-B and readsb for Mere Mortals

Every airliner in the sky above you is
shouting. Several times a second, each
one broadcasts a small radio packet that
says who it is, where it is, how high it
is flying and how fast — its name,
position, altitude and speed, announced
to anyone who cares to listen. The system
is called **ADS-B**, the frequency is
**1090 MHz**, and the broadcasts are not
encrypted, scrambled or access-controlled
in any way. They are a safety system, and
openness is the design: any cheap radio
dongle and a free program can receive
them, which is why the live flight maps
on the internet are mostly fed by
volunteers' kitchen-table receivers.

The program this guide teaches is
**readsb**: a decoder that takes the raw
signal from a dongle (or a data stream
from another receiver), checks and
decodes the packets, tracks every
aircraft it can hear, and serves the
result as tidy files and network streams
that maps and other tools can use.

The lab that wrote this guide had a
handicap worth stating on page one: **it
had no radio.** No dongle, no antenna,
no way to hear a real aircraft. So the
lab did the next most honest thing. It
built readsb from source, then *wrote the
other half of the conversation*: a small
Python program that generates genuine
**Mode S** packets — real format, real
error-checking codes, real position
encoding — for two invented aircraft
flying an invented track, and serves
them to readsb over a network connection
exactly as a second receiver would. Then
it compared what readsb decoded against
the track it had sent, number by number.
All thirteen checks passed, and the
positions agreed to about two
hundred-thousandths of a degree.

That fixture proves the decoding half of
this hobby end to end. The radio half —
dongles, antennas, gain, range — is
taught from the project's own
documentation and clearly labelled
wherever it appears, and `criteria.md`
keeps the full ledger of what was run
and what was only read. The two aircraft
in the lab are fictional, and no real
flight's data appears anywhere in this
guide.

One choice deserves a sentence this
early. Listening is open to everyone by
design, and this guide treats receiving
as the unremarkable act it is. What you
*do* with what you hear — in particular,
whether you feed your receiver's data to
the public aggregator networks — is a
real choice with real trade-offs, and
chapter 11 gives it a fair hearing
before you have to make it.

## What this guide covers

- [**What ADS-B is**](what-adsb-is.md) —
  the broadcast itself: what an aircraft
  announces, how often, and why the
  system is open by design
- [**The moving parts**](the-moving-parts.md) —
  antenna, dongle, decoder, output and
  display: which part holds what, and
  where readsb sits in the chain
- [**The signals in plain terms**](signals-in-plain-terms.md) —
  the 112-bit packet, the message types
  inside it, the error check, and the
  paired-frame trick that turns two
  partial positions into one exact one
- [**Getting and building readsb**](getting-readsb.md) —
  the source build the lab ran, the
  dependency it tripped over, and the
  other ways people install it
- [**Your first decode**](your-first-decode.md) —
  the fixture flight: generating real
  packets for two invented aircraft,
  feeding them to readsb, and checking
  the decoded track against the sent one
- [**Running with a real radio**](running-with-a-radio.md) —
  the dongle run this lab could not do,
  taught from the project's documents:
  device options, gain, ports and the
  service setup
- [**Reading the output**](reading-the-output.md) —
  `aircraft.json` field by field, the
  statistics file, and the wire formats
  (Beast, raw, SBS) other tools speak
- [**Maps — tar1090 and friends**](maps-and-tar1090.md) —
  turning the decoder's files into the
  moving map everyone actually looks at
- [**Antennas, gain and range**](antennas-and-gain.md) —
  why a 6.9 cm antenna hears a whole
  region, why height beats power, and
  why more gain is often worse
- [**Feeding, MLAT and privacy**](feeding-mlat-and-privacy.md) —
  the aggregator networks, how
  multilateration locates aircraft that
  never announce a position, and the
  choice about sharing your data
- [**Decoding it yourself**](decoding-it-yourself.md) —
  one packet taken apart by hand, the
  Beast stream format byte by byte, and
  the Python library that decodes for you
- [**Recipes**](recipes.md) — replay the
  fixture any time, merge two receivers,
  watch your own statistics, and other
  small jobs
- [**The neighbours**](the-neighbours.md) —
  the dump1090 family readsb descends
  from, the ready-made feeder images,
  and the hardware receivers
- [**Limits**](limits.md) — line of
  sight, invisible aircraft, unauthenticated
  broadcasts, and what a fixture cannot
  prove
- [**Troubleshooting**](troubleshooting.md) —
  the missing header file, the position
  that waits for its pair, the parked
  aircraft with a nonsense heading, and
  the other traps this lab met or read
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Building or choosing an SDR from scratch
— the [RTL-SDR guide](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/)
in this series covers the dongle itself.
Other radio hobbies that share the
shelf — weather satellites, digital
voice, general shortwave — each have
their own guides. And nothing here is
aviation advice: this is a receiver for
curiosity and learning, never a source
to fly by.

## How to use this guide

Chapters 1 to 3 are the mental model —
read them before touching anything.
Chapter 4 builds the decoder; chapter 5
decodes a flight you can reproduce
exactly, which is the surest way to know
your build works before a real antenna
enters the story. Chapters 6 to 11 are
the real station, in the order you would
meet its questions. The lab's files live
in `adsb-lab/`: the fixture generator
(`make_fixture.py`), the check script
(`check_decode.py`), the transcripts,
and the `aircraft.json` the decoder
actually wrote.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [RTL-SDR for Mere Mortals](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/)
- [OpenWebRX for Mere Mortals](https://paulsullivan33-dev.github.io/openwebrx-for-mere-mortals/)
- [GNU Radio for Mere Mortals](https://paulsullivan33-dev.github.io/gnu-radio-for-mere-mortals/)
- [Ham Radio for Mere Mortals](https://paulsullivan33-dev.github.io/ham-radio-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/adsb-readsb-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/adsb-readsb-for-mere-mortals/blob/main/LICENSE-CODE).
