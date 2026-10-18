import re
with open("electron/renderer/index.html", "r") as f:
    content = f.read()

# First block: btn-restart-backend (we want to keep the aria-hidden="true")
content = re.sub(
r'<<<<<<< HEAD\n          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">\n=======\n          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">\n>>>>>>> origin/main',
r'          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">',
content)

# Second block: btn-toggle-logs (we want both aria-hidden="true" AND aria-expanded/aria-controls from origin/main)
content = re.sub(
r'<<<<<<< HEAD\n        <button id="btn-toggle-logs" class="toolbar-btn" title="Toggle Console Drawer" aria-label="Toggle Console Drawer">\n          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">\n=======\n        <button id="btn-toggle-logs" class="toolbar-btn" title="Toggle Console Drawer" aria-label="Toggle Console Drawer" aria-expanded="false" aria-controls="logs-drawer">\n          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3">\n>>>>>>> origin/main',
r'        <button id="btn-toggle-logs" class="toolbar-btn" title="Toggle Console Drawer" aria-label="Toggle Console Drawer" aria-expanded="false" aria-controls="logs-drawer">\n          <svg class="sf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">',
content)

# Third block: btn-clear-logs
content = re.sub(
r'<<<<<<< HEAD\n          <button id="btn-clear-logs" class="drawer-btn">Clear</button>\n=======\n          <button id="btn-clear-logs" class="drawer-btn" title="Clear process logs" aria-label="Clear process logs">Clear</button>\n>>>>>>> origin/main',
r'          <button id="btn-clear-logs" class="drawer-btn" title="Clear process logs" aria-label="Clear process logs">Clear</button>',
content)

with open("electron/renderer/index.html", "w") as f:
    f.write(content)
