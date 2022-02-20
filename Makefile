# This makes the documentation and readme for skimpy

.PHONY: all clean site

all: README.md site

# Build the readme
README.md: index.ipynb
		poetry run jupyter nbconvert --to markdown --execute index.ipynb \
		&& rm -rf index_files \
		&& mv index.md README.md \
		&& poetry run python clean_readme.py


# Build the github pages site
site:
		poetry run quarto render --execute

clean:
	rm README.md
