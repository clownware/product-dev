**1. Collection Overview**
- **Purpose**: Give the user an immediate read on their entire collection — what needs attention, what's new, what's running low.
- **Key Content**: Tea grid with name + type, freshness indicator (green/yellow/red), vendor name, quantity remaining, total collection count
- **Primary Action**: Tap a tea to view detail. Secondary: tap "Add tea."
- **Transitions**: App launch → here. Tap tea → Tea Detail. Tap add → Add Tea Form.

**2. Add Tea Form**
- **Purpose**: Capture a new tea with minimal friction — this is the make-or-break screen for adoption.
- **Key Content**: Name field, type selector (green/oolong/black/pu-erh/white/herbal), vendor field with autocomplete from previous entries, quantity, sealed/opened toggle with date
- **Primary Action**: Save the tea. Secondary: cancel.
- **Transitions**: From Overview "Add" button. Save → back to Overview with new tea visible.

**3. Tea Detail**
- **Purpose**: Show everything about one tea — status, provenance, and available actions.
- **Key Content**: Full name + type, vendor name, purchase/open date, days since opened, estimated freshness window, quantity remaining
- **Primary Action**: Mark as "Brewed" (decrements quantity). Secondary: edit details, mark as finished.
- **Transitions**: From Overview tap. Back → Overview.

**Screen Count Check**: 3 screens. This covers the full add → browse → consume cycle from the user flow. The vendor autocomplete in the Add Form handles the vendor-loyalty thread without requiring a dedicated vendor management screen.
