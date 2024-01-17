# This makes the documentation and readme for skimpy

.PHONY: all clean site

all: README.md site

# Build the readme
README.md: docs/index.ipynb
		poetry run jupyter nbconvert --to markdown --execute docs/index.ipynb \
		&& mv docs/index.md README.md \
		&& poetry run python clean_readme.py \
		&& poetry run nbstripout docs/index.ipynb



# Build the github pages site
site:
		poetry run quartodoc build docs/
		poetry run quarto render docs/ --execute
		rm docs/.gitignore
		poetry run pre-commit run --all-files


clean:
	rm README.md
