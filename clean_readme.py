"""
This file takes the automatically generated readme and polishes it a bit by
adding a link to the documentation website. (The logo is part of the centred
block at the top of docs/index.ipynb.)
"""

import re

fname = "README.md"
with open(fname, encoding="utf-8") as f:
    md_text = f.read()
    new_text = re.sub(
        r"`df\.describe\(\)`\.",
        "`df.describe()`.\n[You can find the documentation here](https://aeturrell.github.io/skimpy/).",
        md_text,
    )

with open(fname, "w", encoding="utf-8") as f:
    f.write(new_text)
