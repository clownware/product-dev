**Hypothesis**: We believe that giving tea collectors an at-a-glance inventory view with freshness status and vendor attribution will reduce wasted tea and redundant purchases because collectors currently have no feedback signal between acquiring a tea and discovering it's stale or duplicated.

**Test Signals**:

| Supported | Undermined |
|-----------|------------|
| Users check the app before placing a vendor order | Users add teas but never return to review inventory |
| Users identify and brew teas approaching staleness that they'd otherwise overlooked | Users say they already know what's in their cabinet and don't need a tool |
| Users reference vendor info when deciding to reorder | Users ignore vendor attribution — treat it as noise |

**Riskiest Assumption**: That collectors will add teas at the point of purchase or arrival. If the add-tea flow takes more than a few seconds, the collection stays perpetually incomplete and every downstream feature — freshness tracking, vendor association, inventory awareness — has no foundation. The prototype must test the add-tea entry flow first and measure completion rate and abandonment.
