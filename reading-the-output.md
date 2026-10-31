# Reading the Output

Outcome: you can open `aircraft.json`,
explain every field in it from a real
example, and choose the right wire
format when another program wants your
data.

## aircraft.json, field by field

This is the file everything else eats.
The lab's copy is kept whole at
`adsb-lab/aircraft-final.json`; here is
the moving aircraft's entry at the end
of the fixture run, trimmed of nothing
that matters:

```json
{
    "hex": "abc123",
    "type": "adsb_icao",
    "flight": "FICT1   ",
    "alt_baro": 10200,
    "gs": 399.0,
    "track": 94.02,
    "geom_rate": 0,
    "lat": 33.071501,
    "lon": -96.785291,
    "nic": 8, "rc": 186, "nac_p": 8,
    "seen_pos": 0.038,
    "seen": 0.0,
    "messages": 171,
    "rssi": -6.0,
    "r_dst": 11.609,
    "r_dir": 68.3
}
```

- **hex** — the ICAO address. The key
  everything joins on. (A leading `~`
  would mark an address that did *not*
  come from the aircraft's own
  transponder — a ground system's
  rebroadcast, per the format docs.)
- **type** — where the data came from:
  `adsb_icao` means the aircraft's own
  extended squitters.
- **flight** — the callsign, padded to
  eight characters exactly as broadcast.
- **alt_baro** — pressure altitude in
  feet. (A `geom` altitude, from
  satellite height, appears when the
  aircraft sends TC 20–22 messages.)
- **gs**, **track** — ground speed in
  knots and heading in degrees,
  combined by the decoder from the
  velocity message's two components.
- **geom_rate** — climb/descent in feet
  per minute. Ours reads 0 at the end
  because the fixture's second leg was
  level; mid-climb, the decode log
  showed the sent 512.
- **lat** / **lon** — the latest solved
  position; absent entirely until a CPR
  pair (or a local decode) succeeds.
  TEST2's entry has them; an aircraft
  heard only once would not.
- **seen** / **seen_pos** — seconds
  since any message / since the last
  position. The heartbeat fields: maps
  fade aircraft as these grow, and
  readsb drops the entry altogether
  after a timeout.
- **messages** — how many packets this
  aircraft has contributed since the
  decoder started. The file's top level
  carries the same counter for the
  whole station (364 in the lab's final
  file, 369 by the closing statistics —
  the last seconds of the run sit
  between the two writes, which is
  itself a lesson in reading snapshots).
- **nic**, **nac_p**, **rc** — the
  integrity and accuracy figures the
  aircraft itself reports for its
  position. You did not compute these;
  you are relaying the aircraft's own
  confidence, and the guide's fixture
  honestly shows mid-range values
  because that is what the generator
  encoded.
- **rssi** — received signal strength in
  dBFS. The lab's −6.0 is a fiction of
  the fixture (a fixed byte in the Beast
  frame); on a real station this number
  is diagnostic gold — chapter 10.
- **r_dst** / **r_dir** — distance in
  nautical miles and bearing from *your*
  receiver, which exist only because
  `--lat`/`--lon` were set.

The file is rewritten atomically about
once a second: readers never see a
half-written copy, per the format
documentation shipped in the repo
(`README-json.md`, worth reading whole —
it is the contract tar1090 is built
against).

## The other files

- **receiver.json** — the station's own
  card: readsb version, refresh rate,
  receiver position. Read once at
  startup by anything that cares.
- **stats.json** — counters like the
  ones chapter 5 printed: messages by
  kind, CRC failures, CPR attempts and
  outcomes, signal statistics on a real
  radio. This is the file that answers
  "am I receiving well?" without
  anecdotes.

## The wire formats

Files suit maps; streams suit machines.

- **Beast** (ports 30004/30005) — the
  binary frame format of chapter 12:
  timestamped, compact, lossless. The
  default for receiver-to-receiver and
  receiver-to-feeder traffic, and the
  format the lab's fixture speaks.
- **Raw / AVR** (30001/30002) — each
  packet as a line of hex between `*`
  and `;`, like the `*8dabc123…;` lines
  in chapter 5's log. Human-readable,
  twice the size, beloved of debuggers.
- **SBS** (30003) — comma-separated
  lines in the old BaseStation layout,
  kept alive because a generation of
  tools (and some loggers and plotters)
  still speak nothing else.
- **The JSON port** — one line of JSON
  per position update, for programs
  that want the decoded state without
  polling the file.

Choosing is easy: Beast unless the
other end insists otherwise; AVR when a
human needs to watch; the file when the
consumer is a map or a script of yours.
