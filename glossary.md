# Glossary

Outcome: every term the guide leaned on,
in one line each, in the order you will
look them up after finishing.

- **ADS-B** — Automatic Dependent
  Surveillance–Broadcast: aircraft
  determining their own position (the
  "dependent" part) and broadcasting it
  (the "broadcast" part), automatically.
- **Squitter** — a transponder broadcast
  sent without being asked.
- **Extended squitter** — the 112-bit
  Mode S broadcast (DF 17) that carries
  ADS-B.
- **Mode S** — the transponder protocol
  family with per-aircraft addresses and
  selective interrogation; ADS-B rides
  on its extended squitter.
- **DF (downlink format)** — the 5-bit
  packet-type field; 17 is the one this
  guide lives on.
- **ICAO address** — the 24-bit identity
  assigned to an airframe; printed in
  hex, it is the `hex` key in the JSON.
- **ME field** — the 56-bit payload of
  an extended squitter.
- **Type code (TC)** — the ME field's
  first 5 bits: 1–4 identity, 9–18
  position, 19 velocity.
- **CPR** — Compact Position Reporting:
  positions sent as fractions within a
  grid cell, needing an even/odd pair
  (global decoding) or a reference
  (local decoding) to become a
  coordinate.
- **CRC / parity** — the 24-bit check
  that lets a decoder reject
  noise-damaged packets.
- **Callsign (ident)** — the flight's
  radio name, broadcast in TC 1–4
  messages; not the same as a
  registration.
- **Barometric altitude** — height from
  air pressure against a standard
  datum; the default altitude in the
  data. *Geometric* altitude is the
  satellite-measured kind.
- **Beast** — the binary stream format
  (and originally the hardware) receivers
  use to pass timestamped packets
  between programs.
- **AVR / raw format** — a packet as a
  hex line between `*` and `;`.
- **SBS** — the comma-separated
  BaseStation stream format.
- **Dongle** — the USB SDR receiver,
  usually an RTL-SDR (this series has a
  [guide](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/)
  for it).
- **Gain** — the receiver's
  amplification; too little hides
  aircraft, too much hides them louder.
- **Autogain** — readsb's automatic gain
  adjustment for RTL-SDR devices.
- **RSSI** — received signal strength,
  in dBFS (decibels below full scale).
- **MLAT** — multilateration: fixing a
  position from one transmission's
  arrival times at several receivers.
- **Feeder / aggregator** — a program
  forwarding your stream to a network /
  the network that merges many stations'
  streams into public maps.
- **tar1090** — the web map that draws
  readsb's JSON; the usual companion.
- **Flight level** — altitude in
  hundreds of feet on the standard
  datum: FL350 is 35,000 ft of
  barometric altitude.
- **Fixture** — a known input used to
  prove a system: this guide's invented
  aircraft, real packets.
