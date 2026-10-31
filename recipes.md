# Recipes

Outcome: a handful of complete, small
jobs — each either run in the lab or
built directly from pieces that were.

## 1. Prove any fresh build with the fixture

After building or upgrading readsb,
before touching an antenna:

```
cd adsb-lab
python3 make_fixture.py serve 18112 &
./readsb --net --net-only \
  --net-connector 127.0.0.1,18112,beast_in \
  --write-json /tmp/proof --write-json-every 1 \
  --lat 33.0 --lon -97.0 --no-interactive
# in another shell, after ~20 seconds:
cp /tmp/proof/aircraft.json aircraft-final.json
python3 check_decode.py aircraft-final.json
```

`ALL CHECKS PASSED (13/13)` is the build
certificate. Anything less means the
decoder — not the sky, not the antenna —
needs attention. *(Run in the lab;
this is chapter 5 condensed.)*

## 2. Replay a recorded stream

Any `.beast` file — the lab's fixture or
one recorded from a real station's Beast
output — can be poured back into a
decoder listening on a Beast input port:

```
nc 127.0.0.1 30004 < recording.beast
```

Decoders cannot tell a replay from a
receiver, which is precisely what makes
replays useful for testing maps, feeders
and scripts without an antenna. *(The
fixture file and its framing are lab
artefacts; the port is the standard
one from chapter 6.)*

## 3. Merge a second receiver into yours

A decoder with a better-located dongle —
the attic, a friend's roof across town —
can feed yours instead of competing:

```
# on your readsb, add:
--net-connector attic.example.org,30005,beast_in
```

Your table then holds the union of both
skies, deduplicated by ICAO address, and
tar1090 draws it without knowing there
were ever two radios. This is the
`beast_in` connector of chapter 5 pointed
at a person instead of a Python script.
*(Documented pattern; the mechanism is
the lab-proven one.)*

## 4. Watch your own reception quality

On a real station, once a week:

```
python3 -c "
import json
s = json.load(open('/run/readsb/stats.json'))
print(json.dumps(s, indent=1))" | less
```

Read the CRC failure share, the CPR
success rate and the signal distribution
before and after any antenna change, and
let those — not one afternoon's aircraft
count — judge the change. *(The counters
are the lab-verified ones from chapter
5; the habit is the project's own
advice.)*

## 5. "What is overhead right now?" as a shell one-liner

```
python3 -c "
import json
d = json.load(open('/run/readsb/aircraft.json'))
for a in d['aircraft']:
    if 'lat' in a:
        print(a.get('flight','').strip() or a['hex'],
              a['alt_baro'], 'ft,', a.get('gs','-'), 'kt')"
```

The seed of every "text me when
something interesting passes" project:
the JSON contract of chapter 8 is small
enough to be a hobby in itself. *(Built
against the lab's verified file format;
run it against the fixture JSON to see
it work with no radio at all.)*

## 6. Keep a day of history

```
cp /run/readsb/aircraft.json \
  ~/adsb-log/$(date +%H%M).json   # from cron, hourly
```

Crude, honest archiving: hourly
snapshots of the state file. tar1090's
own history machinery (chapter 9) is
the grown-up version; this is the
version you can explain at 2 a.m.
