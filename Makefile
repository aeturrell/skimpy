# This makes the documentation and readme for skimpy

.PHONY: all clean site publish

all: README.md site

# Build the readme
README.md: docs/index.ipynb
		poetry run jupyter nbconvert --to markdown --execute docs/index.ipynb \
		&& mv docs/index.md README.md \
		&& poetry run python clean_readme.py \
		&& poetry run nbstripout docs/index.ipynb



# Build the github pages site
site:
		poetry run quartodoc build --config docs/_quarto.yml
		cd docs; poetry run quarto render --execute
		rm docs/.gitignore
		poetry run nbstripout docs/*.ipynb
		poetry run pre-commit run --all-files


clean:
	rm README.md



publish:
		cd docs;poetry run quarto publish gh-pages
		rm docs/.gitignore
		poetry run nbstripout docs/*.ipynb
		poetry run pre-commit run --all-files
