# Criteria — what "good" means for this guide

This guide was written and checked
against the same nine-point standard as
the rest of the For Mere Mortals series.
Each criterion is followed by how this
guide meets it, and the verification
ledger at the end states plainly what
was run for real in the lab and what is
documented only — because the difference
matters more than the claims.

1. **Aimed at a stated reader.** A
   reader with one computer and ordinary
   curiosity, wondering what the dots on
   public flight maps are made of. No
   radio licence, no SDR experience, no
   aviation background assumed; the
   [RTL-SDR guide](https://paulsullivan33-dev.github.io/rtl-sdr-for-mere-mortals/)
   in this series is the natural
   companion, not a prerequisite.

2. **An outcome in every chapter.** Each
   chapter opens by naming the concrete
   thing the reader can do or say at its
   end — sketch a packet, prove a build,
   read the JSON — so the guide can be
   skimmed by outcomes alone.

3. **Everything shown was run.** The
   decoder was built from source and fed
   genuine DF17 packets generated in the
   lab; the outputs quoted are the
   decoder's own logs, statistics and
   JSON files, kept in `adsb-lab/`. Where
   the lab could not reach — anything
   requiring an SDR, an antenna, or a
   third-party service — chapters say so
   in their first paragraph, and the
   ledger below separates the two kinds
   of claim.

4. **The data is honest.** All traffic in
   the lab is invented: fictional ICAO
   addresses (abc123, def456), callsigns
   (FICT1, TEST2) and a track over
   made-up coordinates. No real flight's
   data is reproduced anywhere in the
   guide, and the limits chapter states
   why synthetic data must never be fed
   to a public network.

5. **Failures kept, not tidied.** The
   first build's failure (`zstd.h`), the
   first position frame's `CPR decoding:
   none`, and the parked aircraft's
   phantom 303° heading all appear in
   the text where they belong — each is
   the teaching moment of its chapter.

6. **Small, complete, verifiable steps.**
   The centrepiece is a proof, not a
   screenshot: `check_decode.py` compares
   the decoder's output field by field
   against the fixture's intent and
   prints 13/13. Claims a reader cannot
   re-run (feeding, MLAT results, range
   on a real roof) are labelled
   documented and attributed to the
   project's own documentation.

7. **Choices explained, not just made.**
   Why network-input decoding instead of
   a dongle the lab does not have; why
   autogain is the documented default;
   why feeding is a decision and not a
   default — including the privacy facts
   a reader is owed before choosing.

8. **Limits stated.** A dedicated
   chapter: line of sight, equipped
   aircraft only, unauthenticated
   broadcasts, pressure altitude — and
   the guide's own boundary (no radio was
   harmed, or indeed used, in the lab).

9. **The reader can repeat it.** The
   generator, the checker, the captured
   fixture stream and full transcripts
   ship in `adsb-lab/`, with the exact
   versions pinned: readsb 3.16.20 at
   commit 90ece6f. A reader with only a
   laptop can reproduce chapter 5 in an
   afternoon — that reproducibility is
   the point of doing it this way.

## Verification ledger

**Run for real in the lab (evidence in
`adsb-lab/transcripts/`):**

- Cloning wiedehopf/readsb at commit
  `90ece6f` and building it with the
  distribution toolchain — including the
  first failure on the missing `zstd.h`
  header and the successful rebuild
  after installing `libzstd-dev` (t00).
- The full `--help` surface of the built
  binary, 155 lines (t01).
- A pure-Python DF17 generator — real
  CRC, real CPR encoding, real type
  codes — producing two fictional
  aircraft and a 24-step track (t02),
  served as a Beast stream over loopback
  TCP and also captured to
  `adsb-lab/fixture.beast`.
- The live decode run: readsb in
  `--net-only` mode consuming that
  stream — 369 messages received, **0
  bad CRC**, 369 accepted; 291 position
  messages, **289 successful global CPR
  decodes**; clean shutdown (t03).
- The decoder's own `aircraft.json`
  captured from the run
  (`adsb-lab/aircraft-final.json`, t04)
  and the independent comparison:
  **13/13 checks passed**, positions
  agreeing to ~0.00002°, altitude, speed
  and track exact (t05).
- Hand-decoding one packet from the run
  two ways — by hand in chapter 12 and
  programmatically — both agreeing with
  the decoder's own decode (altitude
  10,000 ft; CPR fractions 53521/104494).
- Every fact about the program taken
  from its own README, README-json.md
  and `--help` in the cloned source.

**Documented only (no lab evidence
claimed):**

- Everything involving an actual radio:
  RTL-SDR reception, autogain behaviour,
  antennas, range, real-sky message
  rates. The lab's build was the
  fork's default — RTL-SDR support
  *not* compiled in — and the guide
  says so wherever it matters.
- tar1090's operation (chapter 9): the
  lab produced and verified the JSON it
  consumes, and ran no web server.
- Feeding networks and receiving MLAT
  results (chapter 11): no stream left
  the lab; no account was created.
- pyModeS (chapter 12): named from its
  documentation; the lab's code ran in
  the encoding direction instead.
