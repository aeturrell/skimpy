# This makes the documentation and readme for skimpy

.PHONY: all clean site

all: README.md site

# Build the readme
README.md: index.ipynb
		poetry run jupyter nbconvert --to markdown --execute index.ipynb && mv index.md README.md

# Build the github pages site
site:
		poetry run quarto render --execute

clean:
	rm README.md
