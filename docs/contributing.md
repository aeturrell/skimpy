(contributing)=
# Contributing

Thank you for your interest in improving this project. This project is
open-source under the [MIT license](https://opensource.org/licenses/MIT)
and welcomes contributions in the form of bug reports, feature requests,
and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/aeturrell/skimpy)
- [Documentation](https://aeturrell.github.io/skimpy/)
- [Issue Tracker](https://github.com/aeturrell/skimpy/issues)
- {ref}`code_of_conduct`

## How to report a bug

Report bugs on the [Issue Tracker](https://github.com/aeturrell/skimpy/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case, and/or
steps to reproduce the issue.

## How to request a feature

Request features on the [Issue
Tracker](https://github.com/aeturrell/skimpy/issues).

## How to set up your development environment

You need Python and the following tools:

- [Poetry](https://python-poetry.org/)
- [Nox](https://nox.thea.codes/)
- [nox-poetry](https://nox-poetry.readthedocs.io/)
- [Make](https://www.gnu.org/software/make/)

Before you install poetry, you may wish to run

```bash
poetry config virtualenvs.in-project true
```

to make poetry virtual environments get installed in the project folder. This makes it easier for VS Code to find the project kernel.

Install the package with development requirements:

```bash
$ poetry install
```

You can now run an interactive Python session, or the command-line
interface:

```bash
$ poetry run python
$ poetry run skimpy
```

To build the documentation, you will also need [Make](https://www.gnu.org/software/make/). You can build the docs locally with `make`, which runs a command to build the README and then another to build the website. `make clean` to remove the existing README. (Remember to use pre-commit after updating the documentation.)

## How to test the project

Run the full test suite:

```bash
$ poetry run nox
```

List the available Nox sessions:

```bash
$ poetry run nox --list-sessions
```

You can also run a specific Nox session. For example, invoke the unit
test suite like this:

```bash
$ poetry run nox --session=tests
```

Unit tests are located in the `tests` directory, and are written using
the [pytest](https://pytest.readthedocs.io/) testing framework.

You may need to use, for example, `poetry run nox` to ensure that the
tests are run in the right environment.

For the pre-commit checks, use

```bash
$ poetry run pre-commit run --all-files
```

## How to submit changes

Open a [pull request](https://github.com/aeturrell/skimpy/pulls) to
submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project aims to maintain 96% code
  coverage.
- If your changes add functionality, update the documentation
  accordingly.
- Run make to generate the new documentation.
- Run the pre-commit suite before committing.

Feel free to submit early, though---we can always iterate on this.

To run linting and code formatting checks before committing your change,
you can install pre-commit as a Git hook by running the following
command:

```bash
$ poetry run nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate
your approach.

## How to create a package release

- Open a new branch with the version name

- Change the version in pyproject.toml

- Commit the change with a new version label as the commit message (checking the tests pass)

- Head to github and merge into main

- Draft a new release based on that most recent merge commit, using the new version as the tag

- Confirm the release draft on gitub

- The automatic release github action will push to PyPI.

If you ever need distributable files, you can use the `poetry build` command locally.

## How to build the documentation

- Run `make clean`

- Run `make`

To upload the documentation, it's

```bash
poetry run ghp-import -n -p -f docs/_build/html
```
