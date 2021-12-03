---
title: "skimpy"
author: "A light weight tool for creating summary statistics from dataframes."
markdown:
  variant: markdown_github
---

[![PyPI](https://img.shields.io/pypi/v/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Status](https://img.shields.io/pypi/status/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Python Version](https://img.shields.io/pypi/pyversions/skimpy)](https://pypi.org/project/skimpy)
[![License](https://img.shields.io/pypi/l/skimpy)](https://opensource.org/licenses/MIT)
[![Read the documentation at https://aeturrell.github.io/skimpy/](https://img.shields.io/badge/docs-passing-brightgreen)](https://aeturrell.github.io/skimpy/)
[![Tests](https://github.com/aeturrell/skimpy/workflows/Tests/badge.svg)](https://github.com/aeturrell/skimpy/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/aeturrell/skimpy/branch/main/graph/badge.svg)](https://codecov.io/gh/aeturrell/skimpy)
[![Downloads](https://static.pepy.tech/badge/skimpy)](https://pepy.tech/project/skimpy)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

**skimpy** is a light weight tool that provides
summary statistics about variables in data frames within the console or your interactive Python window.
Think of it as a super-charged version of `df.describe()`.

[\**You can find the full *documentation\* here](https://aeturrell.github.io/skimpy/).\*\*

## Quickstart

_skim_ a dataframe and produce summary statistics within the console
using:

```python
from skimpy import skim

skim(df)
```

where `df` is a dataframe.

If you need to a dataset to try _skimpy_ out on, you can use the
built-in test dataframe:

```python
# | output: asis
from skimpy import skim, generate_test_data

df = generate_test_data()
skim(df)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">╭───────────────────────────────────── skimpy summary ──────────────────────────────────────╮
│ <span style="font-style: italic">         Data Summary         </span> <span style="font-style: italic">      Data Types       </span> <span style="font-style: italic">       Categories        </span>          │
│ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━┓          │
│ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> dataframe         </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Values </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Column Type </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Count </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Categorical Variables </span>┃          │
│ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩ ┡━━━━━━━━━━━━━╇━━━━━━━┩ ┡━━━━━━━━━━━━━━━━━━━━━━━┩          │
│ │ Number of rows    │ 1000   │ │ float64     │ 3     │ │ class                 │          │
│ │ Number of columns │ 10     │ │ category    │ 2     │ │ location              │          │
│ └───────────────────┴────────┘ │ datetime64  │ 2     │ └───────────────────────┘          │
│                                │ int64       │ 1     │                                    │
│                                │ bool        │ 1     │                                    │
│                                │ string      │ 1     │                                    │
│                                └─────────────┴───────┘                                    │
│ <span style="font-style: italic">                                         number                                         </span>  │
│ ┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">        </span>┃<span style="font-weight: bold"> missing </span>┃<span style="font-weight: bold"> complete  </span>┃<span style="font-weight: bold"> mean  </span>┃<span style="font-weight: bold"> sd   </span>┃<span style="font-weight: bold"> p0      </span>┃<span style="font-weight: bold"> p25   </span>┃<span style="font-weight: bold"> p75  </span>┃<span style="font-weight: bold"> p100 </span>┃<span style="font-weight: bold"> hist   </span>┃  │
│ ┃        ┃         ┃<span style="font-weight: bold"> rate      </span>┃       ┃      ┃         ┃       ┃      ┃      ┃        ┃  │
│ ┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">length</span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.5</span> │ <span style="color: #008080; text-decoration-color: #008080">0.36</span> │ <span style="color: #008080; text-decoration-color: #008080">1.6e-06</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.13</span> │ <span style="color: #008080; text-decoration-color: #008080">0.86</span> │ <span style="color: #008080; text-decoration-color: #008080">   1</span> │ <span style="color: #008000; text-decoration-color: #008000">█▃▃▃▄█</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">width </span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">    2</span> │ <span style="color: #008080; text-decoration-color: #008080"> 1.9</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.0021</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.6</span> │ <span style="color: #008080; text-decoration-color: #008080">   3</span> │ <span style="color: #008080; text-decoration-color: #008080">  14</span> │ <span style="color: #008000; text-decoration-color: #008000"> █▃▁  </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">depth </span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">   10</span> │ <span style="color: #008080; text-decoration-color: #008080"> 3.2</span> │ <span style="color: #008080; text-decoration-color: #008080">      2</span> │ <span style="color: #008080; text-decoration-color: #008080">    8</span> │ <span style="color: #008080; text-decoration-color: #008080">  12</span> │ <span style="color: #008080; text-decoration-color: #008080">  20</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▄█▆▃▁</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">rnd   </span> │ <span style="color: #008080; text-decoration-color: #008080">    120</span> │ <span style="color: #008080; text-decoration-color: #008080">     0.88</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.02</span> │ <span style="color: #008080; text-decoration-color: #008080">   1</span> │ <span style="color: #008080; text-decoration-color: #008080">   -2.8</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.74</span> │ <span style="color: #008080; text-decoration-color: #008080">0.66</span> │ <span style="color: #008080; text-decoration-color: #008080"> 3.7</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▄█▅▁ </span> │  │
│ └────────┴─────────┴───────────┴───────┴──────┴─────────┴───────┴──────┴──────┴────────┘  │
│ <span style="font-style: italic">                                        category                                        </span>  │
│ ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                 </span>┃<span style="font-weight: bold"> missing       </span>┃<span style="font-weight: bold"> complete rate          </span>┃<span style="font-weight: bold"> ordered      </span>┃<span style="font-weight: bold"> unique     </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">class          </span> │ <span style="color: #008080; text-decoration-color: #008080">            0</span> │ <span style="color: #008080; text-decoration-color: #008080">                     1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False       </span> │ <span style="color: #008080; text-decoration-color: #008080">         2</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">location       </span> │ <span style="color: #008080; text-decoration-color: #008080">            1</span> │ <span style="color: #008080; text-decoration-color: #008080">                     1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False       </span> │ <span style="color: #008080; text-decoration-color: #008080">         5</span> │  │
│ └─────────────────┴───────────────┴────────────────────────┴──────────────┴────────────┘  │
│ <span style="font-style: italic">                                        datetime                                        </span>  │
│ ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                </span>┃<span style="font-weight: bold"> missing  </span>┃<span style="font-weight: bold"> complete rate   </span>┃<span style="font-weight: bold"> first        </span>┃<span style="font-weight: bold"> last        </span>┃<span style="font-weight: bold"> frequency </span>┃  │
│ ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">date          </span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #008080; text-decoration-color: #008080">              1</span> │ <span style="color: #800000; text-decoration-color: #800000"> 2018-01-31 </span> │ <span style="color: #800000; text-decoration-color: #800000">2101-04-30 </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">M        </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">date_no_freq  </span> │ <span style="color: #008080; text-decoration-color: #008080">       3</span> │ <span style="color: #008080; text-decoration-color: #008080">              1</span> │ <span style="color: #800000; text-decoration-color: #800000"> 1992-01-05 </span> │ <span style="color: #800000; text-decoration-color: #800000">2023-03-04 </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None     </span> │  │
│ └────────────────┴──────────┴─────────────────┴──────────────┴─────────────┴───────────┘  │
│ <span style="font-style: italic">                                         string                                         </span>  │
│ ┏━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">         </span>┃<span style="font-weight: bold"> missing     </span>┃<span style="font-weight: bold"> complete rate       </span>┃<span style="font-weight: bold"> words per row       </span>┃<span style="font-weight: bold"> total words      </span>┃  │
│ ┡━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">text   </span> │ <span style="color: #008080; text-decoration-color: #008080">          6</span> │ <span style="color: #008080; text-decoration-color: #008080">               0.99</span> │ <span style="color: #008080; text-decoration-color: #008080">                5.8</span> │ <span style="color: #008080; text-decoration-color: #008080">            5800</span> │  │
│ └─────────┴─────────────┴─────────────────────┴─────────────────────┴──────────────────┘  │
│ <span style="font-style: italic">                                          bool                                          </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                          </span>┃<span style="font-weight: bold"> true         </span>┃<span style="font-weight: bold"> true rate               </span>┃<span style="font-weight: bold"> hist             </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">booly_col               </span> │ <span style="color: #008080; text-decoration-color: #008080">         520</span> │ <span style="color: #008080; text-decoration-color: #008080">                   0.52</span> │ <span style="color: #008000; text-decoration-color: #008000">     █    █     </span> │  │
│ └──────────────────────────┴──────────────┴─────────────────────────┴──────────────────┘  │
╰─────────────────────────────────────────── End ───────────────────────────────────────────╯
</pre>

It is recommended that you set your datatypes before using _skimpy_ (for example converting any text columns to pandas string datatype), as this will produce richer statistical summaries. However, the _skim_ function will try and guess what the datatypes of your columns are.

**skimpy** also comes with a `clean_columns` function as a convenience. This slugifies column names. For example,

```python
import pandas as pd
from rich import print
from skimpy import clean_columns

columns = [
    "bs lncs;n edbn ",
    "Nín hǎo. Wǒ shì zhōng guó rén",
    "___This is a test___",
    "ÜBER Über German Umlaut",
]
messy_df = pd.DataFrame(columns=columns, index=[0], data=[range(len(columns))])
messy_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>bs lncs;n edbn</th>
      <th>Nín hǎo. Wǒ shì zhōng guó rén</th>
      <th>___This is a test___</th>
      <th>ÜBER Über German Umlaut</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>

Now let's clean these—by default what we get back is in _snake case_:

```python
clean_df = clean_columns(messy_df)
print(list(clean_df.columns))
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">[</span>
    <span style="color: #008000; text-decoration-color: #008000">'bs_lncs_n_edbn'</span>,
    <span style="color: #008000; text-decoration-color: #008000">'nin_hao_wo_shi_zhong_guo_ren'</span>,
    <span style="color: #008000; text-decoration-color: #008000">'this_is_a_test'</span>,
    <span style="color: #008000; text-decoration-color: #008000">'uber_uber_german_umlaut'</span>
<span style="font-weight: bold">]</span>
</pre>

Other naming conventions are available, for example _camel case_:

```python
clean_df = clean_columns(messy_df, case="camel")
print(list(clean_df.columns))
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'bsLncsNEdbn'</span>, <span style="color: #008000; text-decoration-color: #008000">'ninHaoWoShiZhongGuoRen'</span>, <span style="color: #008000; text-decoration-color: #008000">'thisIsATest'</span>, <span style="color: #008000; text-decoration-color: #008000">'uberUberGermanUmlaut'</span><span style="font-weight: bold">]</span>
</pre>

You can find a full list of requirements in the pyproject.toml file. The
main requirements are:

```python
#| echo: false
import toml

config = toml.load("pyproject.toml")
dict_main_deps = config["tool"]["poetry"]["dependencies"]
for key, value in dict_main_deps.items():
    print(f"{key} {value}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">python &gt;=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3.7</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1</span>,&lt;<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4.0</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">click <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">7.1</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">rich ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">10.9</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">pandas ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1.3</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Pygments ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2.10</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">typeguard ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2.12</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1</span>
</pre>

You can try this package out right now in your browser using this
[Google Colab notebook](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)
(requires a Google account). Note that the Google Colab notebook uses the latest package released on PyPI (rather than the development release).

## Installation

You can install the latest release of _skimpy_ via
[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```bash
$ pip install skimpy
```

To install the development version from git, use:

```bash
$ pip install git+https://github.com/aeturrell/skimpy.git
```

For development, see the [Contributor Guide](contributing.html).

## Usage

This package is mostly designed to be used within an interactive console
session or Jupyter notebook

```python
from skimpy import skim

skim(df)
```

However, you can also use it on the command line:

```bash
$ skimpy file.csv
```

## Features

- Support for boolean, numeric, datetime, string, and category
  datatypes
- Command line interface in addition to interactive console
  functionality
- Light weight, with results printed to terminal using the
  [rich](https://github.com/willmcgugan/rich) package.
- Support for different colours for different types of output
- Rounds numerical output to 2 significant figures

_skim_ accepts keyword arguments that change the colour of the top level column headers. For example, to change the colour to magenta, it's

```python
skim(df, header_style="italic magenta")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">╭───────────────────────────────────── skimpy summary ──────────────────────────────────────╮
│ <span style="font-style: italic">         Data Summary         </span> <span style="font-style: italic">      Data Types       </span> <span style="font-style: italic">       Categories        </span>          │
│ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━┓          │
│ ┃<span style="color: #800080; text-decoration-color: #800080; font-style: italic"> dataframe         </span>┃<span style="color: #800080; text-decoration-color: #800080; font-style: italic"> Values </span>┃ ┃<span style="color: #800080; text-decoration-color: #800080; font-style: italic"> Column Type </span>┃<span style="color: #800080; text-decoration-color: #800080; font-style: italic"> Count </span>┃ ┃<span style="color: #800080; text-decoration-color: #800080; font-style: italic"> Categorical Variables </span>┃          │
│ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩ ┡━━━━━━━━━━━━━╇━━━━━━━┩ ┡━━━━━━━━━━━━━━━━━━━━━━━┩          │
│ │ Number of rows    │ 1000   │ │ float64     │ 3     │ │ class                 │          │
│ │ Number of columns │ 10     │ │ category    │ 2     │ │ location              │          │
│ └───────────────────┴────────┘ │ datetime64  │ 2     │ └───────────────────────┘          │
│                                │ int64       │ 1     │                                    │
│                                │ bool        │ 1     │                                    │
│                                │ string      │ 1     │                                    │
│                                └─────────────┴───────┘                                    │
│ <span style="font-style: italic">                                         number                                         </span>  │
│ ┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">        </span>┃<span style="font-weight: bold"> missing </span>┃<span style="font-weight: bold"> complete  </span>┃<span style="font-weight: bold"> mean  </span>┃<span style="font-weight: bold"> sd   </span>┃<span style="font-weight: bold"> p0      </span>┃<span style="font-weight: bold"> p25   </span>┃<span style="font-weight: bold"> p75  </span>┃<span style="font-weight: bold"> p100 </span>┃<span style="font-weight: bold"> hist   </span>┃  │
│ ┃        ┃         ┃<span style="font-weight: bold"> rate      </span>┃       ┃      ┃         ┃       ┃      ┃      ┃        ┃  │
│ ┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">length</span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.5</span> │ <span style="color: #008080; text-decoration-color: #008080">0.36</span> │ <span style="color: #008080; text-decoration-color: #008080">1.6e-06</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.13</span> │ <span style="color: #008080; text-decoration-color: #008080">0.86</span> │ <span style="color: #008080; text-decoration-color: #008080">   1</span> │ <span style="color: #008000; text-decoration-color: #008000">█▃▃▃▄█</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">width </span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">    2</span> │ <span style="color: #008080; text-decoration-color: #008080"> 1.9</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.0021</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.6</span> │ <span style="color: #008080; text-decoration-color: #008080">   3</span> │ <span style="color: #008080; text-decoration-color: #008080">  14</span> │ <span style="color: #008000; text-decoration-color: #008000"> █▃▁  </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">depth </span> │ <span style="color: #008080; text-decoration-color: #008080">      0</span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">   10</span> │ <span style="color: #008080; text-decoration-color: #008080"> 3.2</span> │ <span style="color: #008080; text-decoration-color: #008080">      2</span> │ <span style="color: #008080; text-decoration-color: #008080">    8</span> │ <span style="color: #008080; text-decoration-color: #008080">  12</span> │ <span style="color: #008080; text-decoration-color: #008080">  20</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▄█▆▃▁</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">rnd   </span> │ <span style="color: #008080; text-decoration-color: #008080">    120</span> │ <span style="color: #008080; text-decoration-color: #008080">     0.88</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.02</span> │ <span style="color: #008080; text-decoration-color: #008080">   1</span> │ <span style="color: #008080; text-decoration-color: #008080">   -2.8</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.74</span> │ <span style="color: #008080; text-decoration-color: #008080">0.66</span> │ <span style="color: #008080; text-decoration-color: #008080"> 3.7</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▄█▅▁ </span> │  │
│ └────────┴─────────┴───────────┴───────┴──────┴─────────┴───────┴──────┴──────┴────────┘  │
│ <span style="font-style: italic">                                        category                                        </span>  │
│ ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                 </span>┃<span style="font-weight: bold"> missing       </span>┃<span style="font-weight: bold"> complete rate          </span>┃<span style="font-weight: bold"> ordered      </span>┃<span style="font-weight: bold"> unique     </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">class          </span> │ <span style="color: #008080; text-decoration-color: #008080">            0</span> │ <span style="color: #008080; text-decoration-color: #008080">                     1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False       </span> │ <span style="color: #008080; text-decoration-color: #008080">         2</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">location       </span> │ <span style="color: #008080; text-decoration-color: #008080">            1</span> │ <span style="color: #008080; text-decoration-color: #008080">                     1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False       </span> │ <span style="color: #008080; text-decoration-color: #008080">         5</span> │  │
│ └─────────────────┴───────────────┴────────────────────────┴──────────────┴────────────┘  │
│ <span style="font-style: italic">                                        datetime                                        </span>  │
│ ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                </span>┃<span style="font-weight: bold"> missing  </span>┃<span style="font-weight: bold"> complete rate   </span>┃<span style="font-weight: bold"> first        </span>┃<span style="font-weight: bold"> last        </span>┃<span style="font-weight: bold"> frequency </span>┃  │
│ ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">date          </span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #008080; text-decoration-color: #008080">              1</span> │ <span style="color: #800000; text-decoration-color: #800000"> 2018-01-31 </span> │ <span style="color: #800000; text-decoration-color: #800000">2101-04-30 </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">M        </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">date_no_freq  </span> │ <span style="color: #008080; text-decoration-color: #008080">       3</span> │ <span style="color: #008080; text-decoration-color: #008080">              1</span> │ <span style="color: #800000; text-decoration-color: #800000"> 1992-01-05 </span> │ <span style="color: #800000; text-decoration-color: #800000">2023-03-04 </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None     </span> │  │
│ └────────────────┴──────────┴─────────────────┴──────────────┴─────────────┴───────────┘  │
│ <span style="font-style: italic">                                         string                                         </span>  │
│ ┏━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">         </span>┃<span style="font-weight: bold"> missing     </span>┃<span style="font-weight: bold"> complete rate       </span>┃<span style="font-weight: bold"> words per row       </span>┃<span style="font-weight: bold"> total words      </span>┃  │
│ ┡━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">text   </span> │ <span style="color: #008080; text-decoration-color: #008080">          6</span> │ <span style="color: #008080; text-decoration-color: #008080">               0.99</span> │ <span style="color: #008080; text-decoration-color: #008080">                5.8</span> │ <span style="color: #008080; text-decoration-color: #008080">            5800</span> │  │
│ └─────────┴─────────────┴─────────────────────┴─────────────────────┴──────────────────┘  │
│ <span style="font-style: italic">                                          bool                                          </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">                          </span>┃<span style="font-weight: bold"> true         </span>┃<span style="font-weight: bold"> true rate               </span>┃<span style="font-weight: bold"> hist             </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">booly_col               </span> │ <span style="color: #008080; text-decoration-color: #008080">         520</span> │ <span style="color: #008080; text-decoration-color: #008080">                   0.52</span> │ <span style="color: #008000; text-decoration-color: #008000">     █    █     </span> │  │
│ └──────────────────────────┴──────────────┴─────────────────────────┴──────────────────┘  │
╰─────────────────────────────────────────── End ───────────────────────────────────────────╯
</pre>

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide](CONTRIBUTING.html).

Note that you will need [Quarto](https://quarto.org/) and [Make](https://www.gnu.org/software/make/) installed to build the docs. You can preview the docs using `poetry run quarto preview --execute`. You can build them with `make`.

## License

Distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT), _skimpy_ is free and open source software. You can find the license [here](LICENSE.html)

## Issues

If you encounter any problems, please [file an issue](https://github.com/aeturrell/skimpy/issues) along with a detailed description.

## Credits

This project was generated from [\@cjolowicz](https://github.com/cjolowicz)\'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.

skimpy was inspired by the R package [skimr](https://docs.ropensci.org/skimr/articles/skimr.html) and by exploratory Python packages including [pandas_profiling](https://pandas-profiling.github.io/pandas-profiling) and [dataprep](https://dataprep.ai/), from which the `clean_columns` function comes.

The package is built with [poetry](https://python-poetry.org/), while the documentation is built with [Quarto](https://quarto.org/). Tests are run with [nox](https://nox.thea.codes/en/stable/).
