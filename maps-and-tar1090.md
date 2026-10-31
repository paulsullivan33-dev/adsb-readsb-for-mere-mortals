# Maps — tar1090 and Friends

Outcome: you know what draws the map,
what it eats, and what it adds beyond
dots — and the exact extent of this
guide's evidence about it.

Nobody frames `aircraft.json`. The
picture everyone means by "my receiver"
is a map: aircraft as little aeroplane
icons, labelled, trailing coloured
tracks, updating every second. That
picture is drawn by a separate program
reading the decoder's output, and the
usual one is **tar1090** — by the same
author as this fork of readsb, designed
against exactly the JSON contract of
chapter 8.

Full disclosure, in the pattern of this
guide: **the lab did not run tar1090.**
It produced the `aircraft.json` the map
consumes, verified that file to the last
field, and stopped there. This chapter
is documented-only — from the readsb and
tar1090 projects' own documentation —
and claims nothing more.

## How the pieces fit

tar1090 is a web page plus a small
amount of serving plumbing. A web server
(typically the one the install script
sets up) publishes the page and the
decoder's JSON directory side by side;
your browser polls `aircraft.json`
about once a second and redraws. There
is no database and no server-side state —
which is why the "map is down" faults
are almost always "the JSON stopped
updating" (decoder) or "the page cannot
reach the JSON" (web server), and the
fixture in chapter 5 remains the fastest
way to separate them.

The standard install pairs the two
programs: readsb writes to `/run/readsb`,
tar1090 is configured to read there, and
the author's installer will set up both
in one pass.

## What the map adds

- **Identity enrichment.** A downloadable
  aircraft database (the tar1090-db
  project) maps ICAO addresses to
  aircraft types and registrations, so
  an icon can be labelled with what the
  aeroplane *is*, not only its address.
  readsb can also load this database
  itself (`--db-file`, per its README)
  to enrich its own output.
- **Tracks and history.** The map keeps
  each aircraft's recent path; readsb's
  *globe* indexing options exist largely
  to serve tar1090 installations that
  record long histories — including, per
  the README, the aggregator sites
  themselves.
- **Ranges and overlays.** Your
  theoretical range rings, computed from
  your receiver position and terrain, so
  "why does coverage stop there?" becomes
  a picture instead of an argument.
- **Multiple receivers.** tar1090 can
  overlay several stations' JSON, the
  display-side twin of the merged
  decoding in chapter 12's recipes.

## The alternatives, honestly

- **dump1090's built-in map** (in the
  FlightAware line) — the older, simpler
  page many PiAware users still see;
  fewer features, nothing to install.
- **The aggregators' own maps** — if you
  feed a network (chapter 11), its
  website shows your traffic merged with
  everyone's, which is both more complete
  and not yours.
- **Your own script.** The JSON contract
  is small and stable; a page of Python
  turns it into a text board, a log, or
  a "currently overhead" notifier. For
  many people this is the real hobby,
  and chapter 8 is all the documentation
  it needs.

The map is the reward, but it is worth
remembering what it is: a *rendering*.
Every argument about what an aircraft
did is settled in the JSON and the
packet log, not on the map — one more
place where this guide's
measure-it-don't-admire-it habit pays.
