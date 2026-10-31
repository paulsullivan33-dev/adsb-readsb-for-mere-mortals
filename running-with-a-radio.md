# Running with a Real Radio

Outcome: you know the command line, the
ports and the habits of a real station —
and you know exactly which parts of this
chapter the guide's lab did *not* run.

This is the first fully **documented-only**
chapter, and it says so in its first
paragraph rather than its last. The lab
had no dongle and no antenna; nothing
here was received off the air. What
follows is assembled from readsb's own
documentation — its README and the
`--help` surface the lab did capture —
and it is the standard shape of a real
installation. Where a claim could have
come from the lab, it did; where it
could not, it is the project's word.

## The shape of the real command

Built with `RTLSDR=yes` (chapter 4), the
decoder drives the dongle itself. The
project's own README gives the canonical
example:

```
./readsb --quiet --net --device-type rtlsdr --gain auto
```

- `--device-type rtlsdr` selects the
  radio (it must come before any
  radio-specific options).
- `--gain auto` hands amplification to
  readsb's **autogain**, which the README
  describes as the default behaviour for
  RTL-SDR devices, tuned for ADS-B:
  it watches the signal and adjusts.
  `--gain auto-verbose` logs each change
  while you are learning what your
  location needs. Chapter 10 explains
  the physics it is negotiating.
- `--quiet` silences the per-packet
  narration that made chapter 5's log so
  instructive — you do not want 300
  decodes a minute in a service log.
- `--net` turns on the outputs described
  below.

To that, a real station adds the JSON
directory and its own position, as in
chapter 5: `--write-json /run/readsb`
(by convention a tmpfs directory, since
the files are rewritten every second and
are worthless after a restart) plus
`--lat` and `--lon` for your rooftop —
which feed local CPR decoding, the
distance/direction fields in the JSON,
and every range statistic you will ever
quote.

## The port family

With `--net`, readsb serves the
traditional dump1090-family ports. The
project README's own service example
sets them explicitly:

```
--net-ri-port 30001   raw (AVR) input
--net-ro-port 30002   raw (AVR) output
--net-sbs-port 30003  SBS output
--net-bi-port 30004   Beast input
--net-bo-port 30005   Beast output
```

Memorise the two Beast numbers; they
recur everywhere in this hobby.
**30005 out** is where feeder programs
and other decoders attach to you;
**30004 in** is where another receiver's
stream can be poured into yours — the
same `beast_in` protocol the fixture
used on a private port in chapter 5,
formalised. In this guide's lab all
decoder ports stayed off except that
one contained loopback connection,
which is why the fixture used 18112
rather than squatting on the standard
numbers.

## Running it as a service

Real stations run readsb under systemd,
started at boot, restarted on failure —
the install-script route (chapter 4)
sets this up for you; a hand build means
writing the unit yourself, pointing it
at your long command line. Three habits
distinguish a station from an experiment:

1. **The JSON lives on tmpfs**
   (`/run/readsb`), so a power cut costs
   you nothing and your SD card is not
   rewritten once a second for years.
   tar1090 (chapter 9) is normally
   configured to read exactly there.
2. **The receiver location is set once,
   accurately.** Local CPR and every
   range figure depend on it.
3. **Statistics are kept.** readsb
   writes `stats.json` alongside the
   aircraft file; chapter 8 shows how to
   read your own reception quality from
   it — the honest answer to "is my
   antenna any good?" is in there, not
   in the aircraft count.

Everything in this chapter is one
antenna and one dongle away from having
been the lab's own story — the command
in chapter 5 differs from this one only
in where its input comes from. That is
the quiet strength of the fixture
approach: when your first real run
misbehaves, you will swap the input back
to `make_fixture.py` and learn in one
minute whether the decoder or the sky
is at fault.
