# Troubleshooting

Outcome: the failures this lab actually
met, plus the classic ones from the
project's documentation, each with the
check that separates it from its
neighbours.

## The build stops at `zstd.h`

```
fatal error: zstd.h: No such file or directory
```

A header is missing, not a library: the
runtime zstd is present on most systems,
but compiling needs the **development**
package. `apt-get install libzstd-dev`,
then rebuild. The general shape of this
trap — *runtime installed, headers not*
— accounts for most failed builds of
most C programs; read the first error,
not the fiftieth. *(Met in the lab;
transcript t00.)*

## Aircraft appear, but with no position

You have identification and altitude,
`lat`/`lon` never arrive, and the log
shows `CPR decoding: none`. Almost
always this is chapter 3, not a fault:
a single CPR frame is ambiguous by
design, and a position needs the even
*and* odd frames of a pair. At the edge
of coverage — or from a fixture sending
only one kind — pairs go missing. Check
the statistics: if "global CPR attempts
with valid positions" climbs while you
watch, decoding is healthy and the
aircraft are simply far away. If your
receiver `--lat`/`--lon` are wrong,
nearby local decoding degrades too —
the decoder told the lab "location
accuracy: exact" because the lab told
*it* the truth.

## A parked aircraft shows a heading (or a speed)

The lab's stationary TEST2 displayed
`calc_track: 303` — a heading computed
from the position jitter between CPR
frames of a sender that never moved.
Decoders infer tracks from successive
positions; when successive positions
differ only by grid quantisation, the
inference is noise wearing a uniform.
Distrust derived fields for slow or
stationary traffic; the broadcast fields
(`gs`, `track` from a velocity message)
exist only when the aircraft actually
sends them — TEST2's final JSON entry
honestly has neither.

## The decoder runs but hears nothing (real radio)

Documented checks, in the order the
project's community works through them:
dongle visible to the OS at all; the
build actually contains RTL-SDR support
(chapter 4 — a plain `make` in this fork
does **not**); gain not pinned absurdly
low or high (start with `auto`, chapter
10); antenna actually connected and
somewhere with sky. And the separator
this guide exists to give you: swap the
radio input for the fixture
(`make_fixture.py serve` + the chapter 5
command). Fixture decodes, sky doesn't →
the fault is in parts 1–2 of the chain,
and no decoder option will fix it.

## CRC failures dominate the statistics

On a real station, a rising share of
"invalid CRC" means packets arrive
damaged: weak signals at the range edge
(some is normal), an overloaded front
end (lower the gain or add the filter
of chapter 10), or interference. On a
*fixture*, CRC failures mean your
generator's arithmetic is wrong — the
decoder is the strictest test harness
your packet code will ever meet, and
the lab's 369-for-369 was earned by
getting the polynomial right.

## Messages counted, map empty

The decoder's JSON updates but tar1090
shows nothing: the map reads a directory
the decoder is not writing (check
`--write-json` against the web server's
expectation — the standard pair agree on
`/run/readsb`), or the browser cannot
reach the JSON path. Chapter 9's rule
settles it in one step: open
`aircraft.json` itself. Fresh file, no
map → the web half. Stale file → the
decoder half.

## "Normal exit" that wasn't

Ports and processes: readsb logs
`Normal exit. uptime: …` when it shuts
down cleanly — the lab's run ends with
exactly that line. A second instance
started "to test something" while the
service still holds its ports is the
commonest cause of silent no-output
runs; check who owns the port before
checking anything else.
