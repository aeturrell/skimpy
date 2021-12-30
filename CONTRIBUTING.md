---
title: Contributing
---

Thank you for your interest in improving this project. This project is
open-source under the [MIT license](https://opensource.org/licenses/MIT)
and welcomes contributions in the form of bug reports, feature requests,
and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/aeturrell/skimpy)
- [Documentation](https://skimpy.readthedocs.io/)
- [Issue Tracker](https://github.com/aeturrell/skimpy/issues)
- [Code of Conduct](code_of_conduct.html)

# How to report a bug

Report bugs on the [Issue
Tracker](https://github.com/aeturrell/skimpy/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case, and/or
steps to reproduce the issue.

# How to request a feature

Request features on the [Issue
Tracker](https://github.com/aeturrell/skimpy/issues).

# How to set up your development environment

You need Python and the following tools:

- [Poetry](https://python-poetry.org/)
- [Nox](https://nox.thea.codes/)
- [nox-poetry](https://nox-poetry.readthedocs.io/)
- [Quarto](https://quarto.org/)
- [Make](https://www.gnu.org/software/make/)

Install the package with development requirements:

```{.console}
$ poetry install
```

You can now run an interactive Python session, or the command-line
interface:

```{.console}
$ poetry run python
$ poetry run skimpy
```

To build the documentation, you will also need [Quarto](https://quarto.org/) and [Make](https://www.gnu.org/software/make/). You can preview the docs using `poetry run quarto preview --execute`. You can build them with `make`, which runs

```bash
poetry run jupyter nbconvert --to markdown --execute index.ipynb && mv index.md README.md
```

to build the readme and

```bash
poetry run quarto render --execute
```

to build the documentation website behind the scenes.

# How to test the project

Run the full test suite:

```{.console}
$ poetry run nox
```

List the available Nox sessions:

```{.console}
$ poetry run nox --list-sessions
```

You can also run a specific Nox session. For example, invoke the unit
test suite like this:

```{.console}
$ poetry run nox --session=tests
```

Unit tests are located in the `tests` directory, and are written using
the [pytest](https://pytest.readthedocs.io/) testing framework.

You may need to use, for example, `poetry run nox` to ensure that the
tests are run in the right environment.

For the pre-commit checks, use

```{.console}
$ poetry run pre-commit run --all-files
```

# How to submit changes

Open a [pull request](https://github.com/aeturrell/skimpy/pulls) to
submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project aims to maintain 100% code
  coverage.
- If your changes add functionality, update the documentation
  accordingly.
- Run make to generate the new documentation.
- Run the pre-commit suite before committing.

Feel free to submit early, though---we can always iterate on this.

To run linting and code formatting checks before commiting your change,
you can install pre-commit as a Git hook by running the following
command:

```{.console}
$ poetry run nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate
your approach.
