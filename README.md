# Skimpy

A light weight tool for creating summary statistics from dataframes.
![png](docs/logo.png)

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

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

[![Soure](https://img.shields.io/badge/source%20code-github-lightgrey?style=for-the-badge)](https://github.com/aeturrell/skimpy)

**skimpy** is a light weight tool that provides
summary statistics about variables in **pandas** or **Polars** data frames within the console or your interactive Python window.
Think of it as a super-charged version of **pandas**' `df.describe()`.
[You can find the documentation here](https://aeturrell.github.io/skimpy/).

## Quickstart

_skim_ a **Pandas** dataframe and produce summary statistics within the console
using:

```python
from skimpy import skim

skim(df)
```

where `df` is a dataframe. Alternatively, use `skim_polars()` on **Polars** dataframes.

If you need to a dataset to try _skimpy_ out on, you can use the
built-in test **Pandas** data frame:

```python
from skimpy import skim, generate_test_data

df = generate_test_data()
skim(df)
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">╭──────────────────────────────────────────────── skimpy summary ─────────────────────────────────────────────────╮
│ <span style="font-style: italic">         Data Summary         </span> <span style="font-style: italic">      Data Types       </span> <span style="font-style: italic">       Categories        </span>                                │
│ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━┓                                │
│ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> dataframe         </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Values </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Column Type </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Count </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Categorical Variables </span>┃                                │
│ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩ ┡━━━━━━━━━━━━━╇━━━━━━━┩ ┡━━━━━━━━━━━━━━━━━━━━━━━┩                                │
│ │ Number of rows    │ 1000   │ │ float64     │ 3     │ │ class                 │                                │
│ │ Number of columns │ 13     │ │ category    │ 2     │ │ location              │                                │
│ └───────────────────┴────────┘ │ datetime64  │ 2     │ └───────────────────────┘                                │
│                                │ object      │ 2     │                                                          │
│                                │ int64       │ 1     │                                                          │
│                                │ bool        │ 1     │                                                          │
│                                │ string      │ 1     │                                                          │
│                                │ timedelta64 │ 1     │                                                          │
│                                └─────────────┴───────┘                                                          │
│ <span style="font-style: italic">                                                    number                                                    </span>  │
│ ┏━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name    </span>┃<span style="font-weight: bold"> NA   </span>┃<span style="font-weight: bold"> NA %   </span>┃<span style="font-weight: bold"> mean    </span>┃<span style="font-weight: bold"> sd    </span>┃<span style="font-weight: bold"> p0        </span>┃<span style="font-weight: bold"> p25    </span>┃<span style="font-weight: bold"> p50       </span>┃<span style="font-weight: bold"> p75   </span>┃<span style="font-weight: bold"> p100  </span>┃<span style="font-weight: bold"> hist   </span>┃  │
│ ┡━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">length        </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">     0</span> │ <span style="color: #008080; text-decoration-color: #008080">    0.5</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.36</span> │ <span style="color: #008080; text-decoration-color: #008080">  1.6e-06</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.13</span> │ <span style="color: #008080; text-decoration-color: #008080">      0.5</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.86</span> │ <span style="color: #008080; text-decoration-color: #008080">    1</span> │ <span style="color: #008000; text-decoration-color: #008000">▇▃▃▃▅▇</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">width         </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">     0</span> │ <span style="color: #008080; text-decoration-color: #008080">      2</span> │ <span style="color: #008080; text-decoration-color: #008080">  1.9</span> │ <span style="color: #008080; text-decoration-color: #008080">   0.0021</span> │ <span style="color: #008080; text-decoration-color: #008080">   0.6</span> │ <span style="color: #008080; text-decoration-color: #008080">      1.5</span> │ <span style="color: #008080; text-decoration-color: #008080">    3</span> │ <span style="color: #008080; text-decoration-color: #008080">   14</span> │ <span style="color: #008000; text-decoration-color: #008000"> ▇▃▁  </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">depth         </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">     0</span> │ <span style="color: #008080; text-decoration-color: #008080">     10</span> │ <span style="color: #008080; text-decoration-color: #008080">  3.2</span> │ <span style="color: #008080; text-decoration-color: #008080">        2</span> │ <span style="color: #008080; text-decoration-color: #008080">     8</span> │ <span style="color: #008080; text-decoration-color: #008080">       10</span> │ <span style="color: #008080; text-decoration-color: #008080">   12</span> │ <span style="color: #008080; text-decoration-color: #008080">   20</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▃▇▆▃▁</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">rnd           </span> │ <span style="color: #008080; text-decoration-color: #008080"> 118</span> │ <span style="color: #008080; text-decoration-color: #008080">  11.8</span> │ <span style="color: #008080; text-decoration-color: #008080">  -0.02</span> │ <span style="color: #008080; text-decoration-color: #008080">    1</span> │ <span style="color: #008080; text-decoration-color: #008080">     -2.8</span> │ <span style="color: #008080; text-decoration-color: #008080"> -0.74</span> │ <span style="color: #008080; text-decoration-color: #008080"> -0.00077</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.66</span> │ <span style="color: #008080; text-decoration-color: #008080">  3.7</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▅▇▅▁ </span> │  │
│ └────────────────┴──────┴────────┴─────────┴───────┴───────────┴────────┴───────────┴───────┴───────┴────────┘  │
│ <span style="font-style: italic">                                                   category                                                   </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name                      </span>┃<span style="font-weight: bold"> NA        </span>┃<span style="font-weight: bold"> NA %           </span>┃<span style="font-weight: bold"> ordered               </span>┃<span style="font-weight: bold"> unique             </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">class                           </span> │ <span style="color: #008080; text-decoration-color: #008080">        0</span> │ <span style="color: #008080; text-decoration-color: #008080">             0</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False                </span> │ <span style="color: #008080; text-decoration-color: #008080">                 2</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">location                        </span> │ <span style="color: #008080; text-decoration-color: #008080">        1</span> │ <span style="color: #008080; text-decoration-color: #008080">           0.1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False                </span> │ <span style="color: #008080; text-decoration-color: #008080">                 5</span> │  │
│ └──────────────────────────────────┴───────────┴────────────────┴───────────────────────┴────────────────────┘  │
│ <span style="font-style: italic">                                                     bool                                                     </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name                        </span>┃<span style="font-weight: bold"> true            </span>┃<span style="font-weight: bold"> true rate                     </span>┃<span style="font-weight: bold"> hist                </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">booly_col                         </span> │ <span style="color: #008080; text-decoration-color: #008080">            516</span> │ <span style="color: #008080; text-decoration-color: #008080">                         0.52</span> │ <span style="color: #008000; text-decoration-color: #008000">      ▇    ▇       </span> │  │
│ └────────────────────────────────────┴─────────────────┴───────────────────────────────┴─────────────────────┘  │
│ <span style="font-style: italic">                                                   datetime                                                   </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name                  </span>┃<span style="font-weight: bold"> NA    </span>┃<span style="font-weight: bold"> NA %     </span>┃<span style="font-weight: bold"> first              </span>┃<span style="font-weight: bold"> last              </span>┃<span style="font-weight: bold"> frequency       </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime                    </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #800000; text-decoration-color: #800000">    2018-01-31    </span> │ <span style="color: #800000; text-decoration-color: #800000">   2101-04-30    </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">M              </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime_no_freq            </span> │ <span style="color: #008080; text-decoration-color: #008080">    3</span> │ <span style="color: #008080; text-decoration-color: #008080">     0.3</span> │ <span style="color: #800000; text-decoration-color: #800000">    1992-01-05    </span> │ <span style="color: #800000; text-decoration-color: #800000">   2023-03-04    </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None           </span> │  │
│ └──────────────────────────────┴───────┴──────────┴────────────────────┴───────────────────┴─────────────────┘  │
│ <span style="font-style: italic">                                           &lt;class 'datetime.date'&gt;                                            </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name                      </span>┃<span style="font-weight: bold"> NA    </span>┃<span style="font-weight: bold"> NA %     </span>┃<span style="font-weight: bold"> first            </span>┃<span style="font-weight: bold"> last             </span>┃<span style="font-weight: bold"> frequency      </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date                   </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2018-01-31      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2101-04-30      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">M             </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date_no_freq           </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">1992-01-05      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2023-03-04      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None          </span> │  │
│ └──────────────────────────────────┴───────┴──────────┴──────────────────┴──────────────────┴────────────────┘  │
│ <span style="font-style: italic">                                                 timedelta64                                                  </span>  │
│ ┏━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name     </span>┃<span style="font-weight: bold"> NA   </span>┃<span style="font-weight: bold"> NA %   </span>┃<span style="font-weight: bold"> mean                       </span>┃<span style="font-weight: bold"> median               </span>┃<span style="font-weight: bold"> max                  </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">time diff      </span> │ <span style="color: #008080; text-decoration-color: #008080">   5</span> │ <span style="color: #008080; text-decoration-color: #008080">   0.5</span> │ <span style="color: #008080; text-decoration-color: #008080"> 8 days 00:05:47.336683417</span> │ <span style="color: #008080; text-decoration-color: #008080">     0 days 00:00:00</span> │ <span style="color: #008080; text-decoration-color: #008080">    26 days 00:00:00</span> │  │
│ └─────────────────┴──────┴────────┴────────────────────────────┴──────────────────────┴──────────────────────┘  │
│ <span style="font-style: italic">                                                    string                                                    </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column_name               </span>┃<span style="font-weight: bold"> NA      </span>┃<span style="font-weight: bold"> NA %       </span>┃<span style="font-weight: bold"> words per row                </span>┃<span style="font-weight: bold"> total words              </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">text                     </span> │ <span style="color: #008080; text-decoration-color: #008080">      6</span> │ <span style="color: #008080; text-decoration-color: #008080">       0.6</span> │ <span style="color: #008080; text-decoration-color: #008080">                         5.8</span> │ <span style="color: #008080; text-decoration-color: #008080">                    5761</span> │  │
│ └───────────────────────────┴─────────┴────────────┴──────────────────────────────┴──────────────────────────┘  │
╰────────────────────────────────────────────────────── End ──────────────────────────────────────────────────────╯
</pre>

It is recommended that you set your datatypes before using _skimpy_ (for example converting any text columns to pandas string datatype), as this will produce richer statistical summaries. However, the _skim_ function will try and guess what the datatypes of your columns are.

**skimpy** also comes with a `clean_columns` function as a convenience (with thanks to the [**dataprep**](https://dataprep.ai/) package). This slugifies column names. For example,

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
print("Column names:")
print(list(messy_df.columns))
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Column names:
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'bs lncs;n edbn '</span>, <span style="color: #008000; text-decoration-color: #008000">'Nín hǎo. Wǒ shì zhōng guó rén'</span>, <span style="color: #008000; text-decoration-color: #008000">'___This is a test___'</span>, <span style="color: #008000; text-decoration-color: #008000">'ÜBER Über German Umlaut'</span><span style="font-weight: bold">]</span>
</pre>

Now let's clean these—by default what we get back is in _snake case_:

```python
clean_df = clean_columns(messy_df)
print(list(clean_df.columns))
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'bs_lncs_n_edbn'</span>, <span style="color: #008000; text-decoration-color: #008000">'nin_hao_wo_shi_zhong_guo_ren'</span>, <span style="color: #008000; text-decoration-color: #008000">'this_is_a_test'</span>, <span style="color: #008000; text-decoration-color: #008000">'uber_uber_german_umlaut'</span><span style="font-weight: bold">]</span>
</pre>

Other naming conventions are available, for example _camel case_:

```python
clean_df = clean_columns(messy_df, case="camel")
print(list(clean_df.columns))
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'bsLncsNEdbn'</span>, <span style="color: #008000; text-decoration-color: #008000">'ninHaoWoShiZhongGuoRen'</span>, <span style="color: #008000; text-decoration-color: #008000">'thisIsATest'</span>, <span style="color: #008000; text-decoration-color: #008000">'uberUberGermanUmlaut'</span><span style="font-weight: bold">]</span>
</pre>

## Requirements

You can find a full list of requirements in the [pyproject.toml](https://github.com/aeturrell/skimpy/blob/main/pyproject.toml) file. The
main requirements are:

```python
import toml
from pathlib import Path

config = toml.load(Path("../pyproject.toml"))
dict_main_deps = config["tool"]["poetry"]["dependencies"]
for key, value in dict_main_deps.items():
    print(f"{key} {value}")
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">python &gt;=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3.8</span>,&lt;<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4.0</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">click ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">8.1</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">6</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">rich &gt;=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">10.9</span>,&lt;<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">14.0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">pandas ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2.0</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">3</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Pygments ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2.10</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">jupyter ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1.0</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">ipykernel ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">6.7</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">0</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">numpy ^<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1.22</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">2</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">typeguard <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4.1</span>.<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">4</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">polars <span style="font-weight: bold">{</span><span style="color: #008000; text-decoration-color: #008000">'version'</span>: <span style="color: #008000; text-decoration-color: #008000">'^0.19.0'</span>, <span style="color: #008000; text-decoration-color: #008000">'optional'</span>: <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">True</span><span style="font-weight: bold">}</span>
</pre>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">pyarrow <span style="font-weight: bold">{</span><span style="color: #008000; text-decoration-color: #008000">'version'</span>: <span style="color: #008000; text-decoration-color: #008000">'^13.0.0'</span>, <span style="color: #008000; text-decoration-color: #008000">'optional'</span>: <span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">True</span><span style="font-weight: bold">}</span>
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

For development, see {ref}`contributing`.

## Use

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
- Rounds numerical output to 2 significant figures

## Contributing

Contributions are very welcome. To learn more, see the page on {ref}`contributing`.

Note that you will need [Make](https://www.gnu.org/software/make/) installed to build the docs automatically

## License

Distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT), _skimpy_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/aeturrell/skimpy/issues) along with a detailed description.

## Credits

This project was generated from [\@cjolowicz](https://github.com/cjolowicz)\'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.

skimpy was inspired by the R package [skimr](https://docs.ropensci.org/skimr/articles/skimr.html) and by exploratory Python packages including [pandas_profiling](https://pandas-profiling.github.io/pandas-profiling) and [dataprep](https://dataprep.ai/), from which the `clean_columns` function comes.

The package is built with [poetry](https://python-poetry.org/), while the documentation is built with [Jupyter Book](https://jupyterbook.org). Tests are run with [nox](https://nox.thea.codes/en/stable/).

Using **skimpy** in your paper? Let us know by raising an issue beginning with "citation" and we'll add it to this page.
