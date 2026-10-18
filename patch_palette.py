with open(".Jules/palette.md", "r") as f:
    content = f.read()

import re
merged = re.sub(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> origin/main', r'\2\n\1', content, flags=re.DOTALL)

with open(".Jules/palette.md", "w") as f:
    f.write(merged)
