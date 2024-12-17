# This makes the documentation and readme for skimpy

.PHONY: all clean site publish

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
		uv run quartodoc build --config docs/_quarto.yml
		cd docs; uv run quarto render --execute
		rm docs/.gitignore
		uv run nbstripout docs/*.ipynb
		uv run pre-commit run --all-files


clean:
	rm README.md


publish:
		uv pip install -e .
		uv run quartodoc build --config docs/_quarto.yml
		cd docs;uv run quarto render --execute
		cd docs;uv run quarto publish gh-pages --no-render
		rm docs/.gitignore
		uv run nbstripout docs/*.ipynb
		uv run pre-commit run --all-files
