import re

fname = "README.md"
with open(fname, encoding="utf-8") as f:
    md_text = f.read()
    new_text = re.sub(
        "(```python\n#\|\secho:\sfalse(.*?)\n```)", "", md_text, flags=re.DOTALL
    )
    new_text = re.sub(
        "(\!\[png\]\(index_files\/index_1_0)",
        "![png](docs/index_files/figure-html/cell-2-output-1",
        new_text,
    )

open(fname, "w").write(new_text)
