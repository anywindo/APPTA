## 2023-10-15 - Interactive Filter Groups & Expandable Sections Accessibility
**Learning:** For desktop-style drawer components and segmented controls built in web tech, screen readers often fail to announce state changes correctly without explicit ARIA attributes. A button acting as an accordion toggle needs `aria-expanded` and `aria-controls`, and dynamic filter groups should use `role="group"` along with `aria-pressed` states on the buttons to indicate which filter is currently active.
**Action:** Add `aria-expanded` attributes mapped to the drawer's state on toggle buttons, and use `aria-pressed` on custom filter/segmented control components moving forward.
## 2026-10-18 - [Scroll Container Focusability]
**Learning:** Elements with `overflow-y: auto` (like terminal outputs or console drawers) are inherently inaccessible to keyboard users unless explicitly made focusable. Without `tabindex="0"`, screen reader and keyboard-only users cannot scroll through the logs.
**Action:** Always verify that custom scroll containers are focusable and semantically labeled with `role="log"` or `role="region"` so they can be discovered and scrolled via keyboard.
