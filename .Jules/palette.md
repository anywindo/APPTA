## 2026-10-12 - Added ARIA attributes to icon-only buttons
**Learning:** Found several icon-only buttons in `electron/renderer/index.html` (e.g. Restart, Toggle Logs, Close Logs) that lacked accessible names.
**Action:** Applied `aria-label` to the buttons and `aria-hidden="true"` to the decorative inner SVG elements so screen readers can correctly identify the buttons' purposes.
