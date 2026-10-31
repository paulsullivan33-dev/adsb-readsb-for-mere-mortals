# Limits

Outcome: you can state, without
prompting, what this system cannot see,
cannot prove and cannot promise —
including the limits of this guide.

**Line of sight is law.** 1090 MHz does
not bend around hills, buildings or the
planet. A station hears a bubble of sky
whose size is set by antenna height and
terrain (chapter 10); outside the
bubble, aircraft are not "filtered" —
they are physically absent. Two stations
20 miles apart honestly disagree about
the sky, and both are right.

**It only hears volunteers.** ADS-B is a
broadcast *by* aircraft *of themselves*.
Anything without a working transponder —
some light aircraft, many gliders,
drones, birds, and anything deliberately
quiet — does not exist in this system.
A clear map is not an empty sky; it is
a map of the equipped and the willing.
MLAT (chapter 11) widens the net to
transponder replies, but it still hears
only what radios say.

**The broadcasts are unauthenticated.**
Nothing in a squitter proves the sender
is the aircraft it claims to be; the
system was designed for cooperation,
not adversaries. In practice the data
is overwhelmingly genuine, but the
format itself cannot tell you so —
anyone with a transmitter (or, as this
guide demonstrates at packet level, a
generator) can speak. Professional
systems cross-check with radar; a lone
receiver should hold its map with
slightly open hands. *This is also why
the fixture in chapter 5 is a fixture:*
synthetic data must never be fed to a
public network as if it were sky.

**Positions are claims with error bars.**
The aircraft reports what its navigation
believes; the CPR grid quantises what it
sends (the lab's decoded positions
differed from the sent ones by about
0.00002°, roughly two metres — honest
precision, not survey grade), and the
decoder's own inferences — like the
parked TEST2's phantom 303° heading —
can be confident nonsense when the input
is noise. Fields carry the aircraft's
own accuracy figures for a reason.

**Altitude is pressure, mostly.** The
headline number is height above a
standard pressure surface, not above
your ground; near an airport it can sit
hundreds of feet from the altimeter
reading you would care about. Geometric
altitude exists, but not every aircraft
sends it.

**And the guide's own limits.** The
decoder was built and proven here; the
radio was not. No claim in this guide
rests on a reception the lab did not
make — but that also means gain,
antennas and range are taught from
documents, and your roof will have the
final word on all three. readsb itself
moves quickly (the lab's commit is a
fortnight's news by the time you read
this); flags drift, and the `--help` of
*your* build outranks any sentence in
this guide — a rule the guide applied to
itself throughout.
