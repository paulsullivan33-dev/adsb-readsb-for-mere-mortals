# Getting and Building readsb

Outcome: you have a `readsb` binary whose
version you can state, built the way
this guide's lab built it — and you know
the other two routes people take, and
what each trades away.

readsb has no official binary releases
to download. It is a C program that
people build from source, or receive
inside someone else's package — a
feeder image, a distribution build, an
install script. The lab used the source
build, because it is the one route where
every step can be shown.

## The family in one paragraph

readsb descends from **dump1090**, the
decoder Salvatore Sanfilippo ("antirez")
wrote in 2012 to prove an SDR point. The
program's own `--help` prints its
credits, and they read as a genealogy:
antirez's original, Malcolm Robb's work,
the mutability fork (which became
FlightAware's dump1090-fa), Mictronics'
readsb, and finally **wiedehopf's
readsb** — the maintained fork this
guide uses, and the one the community
generally builds today. Chapter 13 tells
the story properly; for building, what
matters is the address:

```
git clone https://github.com/wiedehopf/readsb.git
```

The lab cloned on 30 October 2026 and
got commit `90ece6f`, which reports
itself as:

```
readsb version: 3.16.20 wiedehopf git: v3.16.20-17-g90ece6f
```

## The build

The dependencies are a C compiler,
`make`, and a handful of libraries. The
lab's first attempt failed within
seconds, and the failure is worth
keeping verbatim because every builder
meets its twin:

```
fatal error: zstd.h: No such file or directory
compilation terminated.
make: *** [Makefile:189: interactive.o] Error 1
```

`zstd.h` belongs to the **libzstd
development package** — readsb compresses
its history files with zstd, and the
runtime library alone does not include
the header a compiler needs. One package
fixed it:

```
apt-get install libzstd-dev
make -j2
```

and the build ran clean, producing the
`readsb` binary (about 2.5 MB) in the
source tree. The full log, failure
included, is `adsb-lab/transcripts/t00-build.txt`.

## The radio switch you must know about

This fork's Makefile defaults to
`RTLSDR ?= no` — a binary built plainly,
as the lab's was, has **no RTL-SDR
support compiled in**. It can decode
network streams and files, which is all
the lab needed, but it cannot talk to a
dongle. For a real station you install
the SDR library headers first and say so:

```
apt-get install librtlsdr-dev
make -j2 RTLSDR=yes
```

Same source, same program, one more
sense. Check which one you built before
blaming an antenna:

```
./readsb --version     # always works
./readsb --help        # the full option surface
```

That `--help` output runs to 155 lines
and is the program's real manual —
several chapters of this guide teach
flags taken from the lab's own capture
of it (`adsb-lab/transcripts/t01-help.txt`),
not from anyone's summary.

## The other routes (documented)

- **The author's install script.**
  wiedehopf maintains a script that
  installs readsb (and optionally
  tar1090) as a proper service on a
  Raspberry Pi or Debian system, with
  sensible network ports already set.
  Most real stations start here. It is
  also the least inspectable route:
  you are trusting a script, as with
  any `curl | bash`.
- **Feeder images.** FlightAware's
  PiAware image and similar bundles
  ship a working decoder (theirs is
  dump1090-fa) preconfigured with their
  feeder. Fastest path to a live map of
  your own; the decoder is then theirs
  to configure, in their layout.
- **This source build.** Slowest,
  plainest, and the only one where you
  can point at the exact commit doing
  your decoding — which is why a guide
  that intends to prove things uses it.

Whichever route you take, keep the
version string. Every claim in the next
chapter was made against 3.16.20 at the
commit above; decoder behaviour drifts
between versions, and "which readsb?"
is the first question in any honest
troubleshooting.
