skimpy
======

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/skimpy.svg
   :target: https://pypi.org/project/skimpy/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/skimpy.svg
   :target: https://pypi.org/project/skimpy/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/skimpy
   :target: https://pypi.org/project/skimpy
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/skimpy
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/skimpy/latest.svg?label=Read%20the%20Docs
   :target: https://skimpy.readthedocs.io/
   :alt: Read the documentation at https://skimpy.readthedocs.io/
.. |Tests| image:: https://github.com/aeturrell/skimpy/workflows/Tests/badge.svg
   :target: https://github.com/aeturrell/skimpy/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/aeturrell/skimpy/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/aeturrell/skimpy
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Welcome
-------

Welcome to *skimpy*! *skimpy* is a light weight tool that provides summary statistics about variables in data frames within the console. Think of it as a super version of `df.summary()`.

Quickstart
----------

*skim* a dataframe and produce summary statistics within the console using:

.. code:: python

   from skimpy import skim

   skim(df)

If you need to a dataset to try *skimpy* out on, use the in-built one:

.. code:: python

   from skimpy import skim, generate_test_data

   df = generate_test_data()
   skim(df)

It is recommended that you set your datatypes before using *skimpy* (for example converting any text columns to pandas string datatype), as this will produce richer statistical summaries.

Features
--------

* Support for boolean, numeric, datetime, string, and category datatypes
* Command line interface in addition to interactive console functionality
* Light weight, with results printed to terminal using the `rich`_ package.

Requirements
------------

You can find a full list of requirements in the pyproject.toml file. The main requirements are:

* python = ">=3.7.1,<4.0.0"
* click = "^8.0.1"
* rich = "^10.9.0"
* pandas = "^1.3.2"


Installation
------------

You can install the latest release of *skimpy* via pip_ from PyPI_:

.. code:: console

   $ pip install skimpy

To install the development version from git, use:

.. code:: console

   $ pip install git+https://github.com/aeturrell/skimpy.git

For development, see the `Contributor Guide`_.

Usage
-----

This package is mostly designed to be used within an interactive console session or Jupyter notebook

.. code-block:: python

   from skimpy import skim

   skim(df)

However, you can also use it on the command line:

.. code:: console

   $ skimpy file.csv

*skimpy* will do its best to infer column datatypes.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*skimpy* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

skimpy was inspired by the R package `skimr`_ and by exploratory Python packages including `pandas_profiling`_ and `dataprep`_.

.. _@cjolowicz: https://github.com/cjolowicz
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/aeturrell/skimpy/issues
.. _pip: https://pip.pypa.io/
.. _skimr: https://docs.ropensci.org/skimr/articles/skimr.html
.. _pandas_profiling: https://pandas-profiling.github.io/pandas-profiling
.. _dataprep: https://dataprep.ai/
.. _rich: https://github.com/willmcgugan/rich
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
