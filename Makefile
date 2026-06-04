# This makes the documentation and readme for skimpy

.PHONY: all clean site

all: README.md site

# Build the readme
README.md: docs/index.ipynb
		uv pip install -e . \
		&& uv run jupyter nbconvert --to markdown --execute docs/index.ipynb \
		&& mv docs/index.md README.md \
		&& uv run python clean_readme.py \
		&& uv run nbstripout docs/index.ipynb



# Build the github pages site
site:
		uv pip install -e .
		uv run great-docs build
		uv run pre-commit run --all-files


clean:
		rm README.md
		rm -rf great-docs/
