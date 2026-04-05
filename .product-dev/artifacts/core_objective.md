**Core Objective**: Tea collectors can make confident inventory, freshness, and reorder decisions based on current collection state, without relying on memory or manual tracking overhead.

**Success Looks Like**:
- User checks collection status before placing a vendor order (behavior change from blind ordering)
- No teas go stale unnoticed — open teas are consumed or flagged within their quality window (waste reduction)
- User can trace any tea in their cabinet back to the vendor and purchase date within seconds (vendor connection preserved)

**Design Guardrails**:
- Must require less effort to maintain than a spreadsheet — if it feels like data entry, it fails
- Must provide value with incomplete data — partial inventory is better than none, no "all or nothing" cliff
- Must not displace the ritual of browsing the cabinet — the tool augments the experience, not replaces it
