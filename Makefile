.PHONY: all clean

all: index.md


index.md: skimpy-homepage/index.ipynb index.md
		quarto render skimpy-homepage/index.ipynb --to markdown && mv skimpy-homepage/docs/index.md index.md
