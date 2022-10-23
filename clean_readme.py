"""
This file takes the automatically generated readme and polishes it a bit by:
1) adding the logo to the top of the page
2) adding a link to the documentation website
"""
import re

fname = "README.md"
with open(fname, encoding="utf-8") as f:
    md_text = f.read()
    new_text = re.sub(
        "statistics from dataframes\.",
        "statistics from dataframes.\n![png](docs/logo.png)",
        md_text,
        flags=re.DOTALL,
    )
    new_text = re.sub(
        "\`df\.describe\(\)\`\.",
        "`df.describe()`.\n[You can find the documentation here](https://aeturrell.github.io/skimpy/).",
        new_text,
    )

open(fname, "w").write(new_text)
