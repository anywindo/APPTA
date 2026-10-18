## 2023-10-15 - Interactive Filter Groups & Expandable Sections Accessibility
**Learning:** For desktop-style drawer components and segmented controls built in web tech, screen readers often fail to announce state changes correctly without explicit ARIA attributes. A button acting as an accordion toggle needs `aria-expanded` and `aria-controls`, and dynamic filter groups should use `role="group"` along with `aria-pressed` states on the buttons to indicate which filter is currently active.
**Action:** Add `aria-expanded` attributes mapped to the drawer's state on toggle buttons, and use `aria-pressed` on custom filter/segmented control components moving forward.
## 2024-05-24 - Screen Reader Redundancy in Avatar Components
**Learning:** When displaying an avatar image next to the user's name as text, providing an `alt` attribute with the user's name causes screen readers to redundantly announce the name twice (e.g., "Alice, Alice").
**Action:** For decorative avatars accompanied by visible name text, set `alt=""` on the `<img>` and `aria-hidden="true"` on the wrapper to hide the image from assistive technologies, ensuring a clean and concise screen reader experience.
## 2026-10-12 - Added ARIA attributes to icon-only buttons
**Learning:** Found several icon-only buttons in `electron/renderer/index.html` (e.g. Restart, Toggle Logs, Close Logs) that lacked accessible names.
**Action:** Applied `aria-label` to the buttons and `aria-hidden="true"` to the decorative inner SVG elements so screen readers can correctly identify the buttons' purposes.
