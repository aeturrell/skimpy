---
title: skimpy
---

[![PyPI](https://img.shields.io/pypi/v/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Status](https://img.shields.io/pypi/status/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Python Version](https://img.shields.io/pypi/pyversions/skimpy)](https://pypi.org/project/skimpy)
[![License](https://img.shields.io/pypi/l/skimpy)](https://opensource.org/licenses/MIT)

[![Read the documentation at https://github.com/aeturrell/skimpy](https://img.shields.io/readthedocs/skimpy/latest.svg?label=Read%20the%20Docs)](https://github.com/aeturrell/skimpy)
[![Tests](https://github.com/aeturrell/skimpy/workflows/Tests/badge.svg)](https://github.com/aeturrell/skimpy/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/aeturrell/skimpy/branch/main/graph/badge.svg)](https://codecov.io/gh/aeturrell/skimpy)
[![Downloads](https://static.pepy.tech/badge/skimpy)](https://pepy.tech/project/skimpy)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

# Welcome

Welcome to *skimpy*! *skimpy* is a light weight tool that provides
summary statistics about variables in data frames within the console.
Think of it as a super version of [df.describe()]{.title-ref}.

# Quickstart

*skim* a dataframe and produce summary statistics within the console
using:

``` {.python}
from skimpy import skim

skim(df)
```

If you need to a dataset to try *skimpy* out on, you can use the
built-in test dataframe:

``` {.python}
from skimpy import skim, generate_test_data

df = generate_test_data()
skim(df)
```

![image](https://raw.githubusercontent.com/aeturrell/skimpy/master/img/skimpy_example.png){width="600px"}

It is recommended that you set your datatypes before using *skimpy* (for
example converting any text columns to pandas string datatype), as this
will produce richer statistical summaries.

*skim* accepts keyword arguments that change the colour of the datatypes
as displayed. For example, to change the colour of datetimes to be
chartreuse instead of red, the code is:

``` {.python}
skim(df, datetime="chartreuse1")
```

You can also change the colours of the headers of the first three
summary tables using, for example,

``` {.python}
skim(df, header_style="italic green")
```

You can try this package out right now in your browser using this
[Google Colab
notebook](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)
(requires a Google account). Note that the Google Colab notebook uses
the latest package released on PyPI (rather than the development
release).

(Please note that *skimpy* is waiting for a readthedocs site name to
become available.)

# Features

-   Support for boolean, numeric, datetime, string, and category
    datatypes
-   Command line interface in addition to interactive console
    functionality
-   Light weight, with results printed to terminal using the
    [rich](https://github.com/willmcgugan/rich) package.
-   Support for different colours for different types of output
-   Rounds numerical output to 2 significant figures

# Requirements

You can find a full list of requirements in the pyproject.toml file. The
main requirements are:

-   python = \"\>=3.7.1,\<4.0.0\"
-   click = \"\^8.0.1\"
-   rich = \"\^10.9.0\"
-   pandas = \"\^1.3.2\"

# Installation

You can install the latest release of *skimpy* via
[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

``` {.console}
$ pip install skimpy
```

To install the development version from git, use:

``` {.console}
$ pip install git+https://github.com/aeturrell/skimpy.git
```

For development, see the [Contributor Guide](CONTRIBUTING.rst).

# Usage

This package is mostly designed to be used within an interactive console
session or Jupyter notebook

``` {.python}
from skimpy import skim

skim(df)
```

However, you can also use it on the command line:

``` {.console}
$ skimpy file.csv
```

*skimpy* will do its best to infer column datatypes.

# Contributing

Contributions are very welcome. To learn more, see the [Contributor
Guide](CONTRIBUTING.rst).

# License

Distributed under the terms of the [MIT
license](https://opensource.org/licenses/MIT), *skimpy* is free and open
source software.

# Issues

If you encounter any problems, please [file an
issue](https://github.com/aeturrell/skimpy/issues) along with a detailed
description.

# Credits

This project was generated from
[\@cjolowicz](https://github.com/cjolowicz)\'s [Hypermodern Python
Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
template.

skimpy was inspired by the R package
[skimr](https://docs.ropensci.org/skimr/articles/skimr.html) and by
exploratory Python packages including
[pandas_profiling](https://pandas-profiling.github.io/pandas-profiling)
and [dataprep](https://dataprep.ai/).
