**What We're Testing**: Whether collectors will maintain a tea inventory when adding a tea takes seconds and freshness alerts surface without manual checking.

**Included** (must be functional or realistic):
- Add tea flow with vendor autocomplete (tests: input friction — will users actually do this?)
- Collection overview with freshness color indicators (tests: at-a-glance value — do users notice and act on status?)
- Tea detail with "Brewed" action (tests: engagement loop — do users track consumption, not just acquisition?)
- Vendor name displayed on tea cards and detail (tests: whether vendor attribution gets used in decision-making)

**Simulated** (looks real but isn't):
- Pre-populated collection of 10-12 teas across 3 vendors, with varied freshness states (avoids cold-start during testing)
- Freshness calculations hardcoded to fixed dates (no real time tracking engine)
- Vendor autocomplete from a static list (no backend persistence)

**Excluded** (intentionally omitted):
- User accounts and authentication (not testing identity, just behavior)
- Search, filter, or sort within collection (test with a small enough set that browsing works)
- Notifications or push alerts (test whether users check voluntarily before adding nudges)
- Vendor detail pages or reorder links (vendor attribution is in-app context only for now)

**Fidelity Decision**: Medium — interactive tap-through prototype with realistic tea data but no backend. Need real interactions to measure friction, but visual polish doesn't affect hypothesis validation.
