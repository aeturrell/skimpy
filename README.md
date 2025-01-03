# Skimpy

A light weight tool for creating summary statistics from dataframes.
![png](docs/logo.png)

![](logo.png)

[![PyPI](https://img.shields.io/pypi/v/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Status](https://img.shields.io/pypi/status/skimpy.svg)](https://pypi.org/project/skimpy/)
[![Python Version](https://img.shields.io/pypi/pyversions/skimpy)](https://pypi.org/project/skimpy)
[![License](https://img.shields.io/pypi/l/skimpy)](https://opensource.org/licenses/MIT)
[![Read the documentation at https://aeturrell.github.io/skimpy/](https://img.shields.io/badge/docs-passing-brightgreen)](https://aeturrell.github.io/skimpy/)
[![Tests](https://github.com/aeturrell/skimpy/workflows/Tests/badge.svg)](https://github.com/aeturrell/skimpy/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/aeturrell/skimpy/branch/main/graph/badge.svg)](https://codecov.io/gh/aeturrell/skimpy)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)
[![Downloads](https://static.pepy.tech/badge/skimpy)](https://pepy.tech/project/skimpy)
[![Source](https://img.shields.io/badge/source%20code-github-lightgrey?style=for-the-badge)](https://github.com/aeturrell/skimpy)

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)



**skimpy** is a light weight tool that provides summary statistics about variables in **pandas** or **Polars** data frames within the console or your interactive Python window.

Think of it as a super-charged version of **pandas**' `df.describe()`.
[You can find the documentation here](https://aeturrell.github.io/skimpy/).

## Quickstart

`skim` a **pandas** or **polars** dataframe and produce summary statistics within the console
using:

```python
from skimpy import skim

skim(df)
```

where `df` is a **pandas** or **polars** dataframe.

If you need to a dataset to try *skimpy* out on, you can use the built-in test **Pandas** data frame:


```python
from skimpy import generate_test_data, skim

df = generate_test_data()
skim(df)
```


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">╭──────────────────────────────────────────────── skimpy summary ─────────────────────────────────────────────────╮
│ <span style="font-style: italic">         Data Summary         </span> <span style="font-style: italic">      Data Types       </span> <span style="font-style: italic">       Categories        </span>                                │
│ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━┓                                │
│ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Dataframe         </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Values </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Column Type </span>┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Count </span>┃ ┃<span style="color: #008080; text-decoration-color: #008080; font-weight: bold"> Categorical Variables </span>┃                                │
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
│ ┏━━━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column  </span>┃<span style="font-weight: bold"> NA   </span>┃<span style="font-weight: bold"> NA %  </span>┃<span style="font-weight: bold"> mean      </span>┃<span style="font-weight: bold"> sd      </span>┃<span style="font-weight: bold"> p0         </span>┃<span style="font-weight: bold"> p25     </span>┃<span style="font-weight: bold"> p50        </span>┃<span style="font-weight: bold"> p75    </span>┃<span style="font-weight: bold"> p100  </span>┃<span style="font-weight: bold"> hist   </span>┃  │
│ ┡━━━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">length </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">   0.5016</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.3597</span> │ <span style="color: #008080; text-decoration-color: #008080"> 1.573e-06</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.134</span> │ <span style="color: #008080; text-decoration-color: #008080">    0.4976</span> │ <span style="color: #008080; text-decoration-color: #008080">0.8602</span> │ <span style="color: #008080; text-decoration-color: #008080">    1</span> │ <span style="color: #008000; text-decoration-color: #008000">▇▃▃▃▅▇</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">width  </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">    2.037</span> │ <span style="color: #008080; text-decoration-color: #008080">  1.929</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.002057</span> │ <span style="color: #008080; text-decoration-color: #008080">  0.603</span> │ <span style="color: #008080; text-decoration-color: #008080">     1.468</span> │ <span style="color: #008080; text-decoration-color: #008080"> 2.953</span> │ <span style="color: #008080; text-decoration-color: #008080">13.91</span> │ <span style="color: #008000; text-decoration-color: #008000"> ▇▃▁  </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">depth  </span> │ <span style="color: #008080; text-decoration-color: #008080">   0</span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">    10.02</span> │ <span style="color: #008080; text-decoration-color: #008080">  3.208</span> │ <span style="color: #008080; text-decoration-color: #008080">         2</span> │ <span style="color: #008080; text-decoration-color: #008080">      8</span> │ <span style="color: #008080; text-decoration-color: #008080">        10</span> │ <span style="color: #008080; text-decoration-color: #008080">    12</span> │ <span style="color: #008080; text-decoration-color: #008080">   20</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▃▇▆▃▁</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">rnd    </span> │ <span style="color: #008080; text-decoration-color: #008080"> 118</span> │ <span style="color: #008080; text-decoration-color: #008080"> 11.8</span> │ <span style="color: #008080; text-decoration-color: #008080"> -0.01977</span> │ <span style="color: #008080; text-decoration-color: #008080">  1.002</span> │ <span style="color: #008080; text-decoration-color: #008080">    -2.809</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.7355</span> │ <span style="color: #008080; text-decoration-color: #008080">-0.0007736</span> │ <span style="color: #008080; text-decoration-color: #008080">0.6639</span> │ <span style="color: #008080; text-decoration-color: #008080">3.717</span> │ <span style="color: #008000; text-decoration-color: #008000">▁▅▇▅▁ </span> │  │
│ └─────────┴──────┴───────┴───────────┴─────────┴────────────┴─────────┴────────────┴────────┴───────┴────────┘  │
│ <span style="font-style: italic">                                                   category                                                   </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column                      </span>┃<span style="font-weight: bold"> NA         </span>┃<span style="font-weight: bold"> NA %            </span>┃<span style="font-weight: bold"> ordered                 </span>┃<span style="font-weight: bold"> unique              </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">class                      </span> │ <span style="color: #008080; text-decoration-color: #008080">         0</span> │ <span style="color: #008080; text-decoration-color: #008080">              0</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False                  </span> │ <span style="color: #008080; text-decoration-color: #008080">                  2</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">location                   </span> │ <span style="color: #008080; text-decoration-color: #008080">         1</span> │ <span style="color: #008080; text-decoration-color: #008080">            0.1</span> │ <span style="color: #00d7ff; text-decoration-color: #00d7ff">False                  </span> │ <span style="color: #008080; text-decoration-color: #008080">                  5</span> │  │
│ └─────────────────────────────┴────────────┴─────────────────┴─────────────────────────┴─────────────────────┘  │
│ <span style="font-style: italic">                                                     bool                                                     </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column                          </span>┃<span style="font-weight: bold"> true             </span>┃<span style="font-weight: bold"> true rate                      </span>┃<span style="font-weight: bold"> hist                 </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">booly_col                      </span> │ <span style="color: #008080; text-decoration-color: #008080">             516</span> │ <span style="color: #008080; text-decoration-color: #008080">                          0.52</span> │ <span style="color: #008000; text-decoration-color: #008000">       ▇    ▇       </span> │  │
│ └─────────────────────────────────┴──────────────────┴────────────────────────────────┴──────────────────────┘  │
│ <span style="font-style: italic">                                                   datetime                                                   </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column                       </span>┃<span style="font-weight: bold"> NA    </span>┃<span style="font-weight: bold"> NA %     </span>┃<span style="font-weight: bold"> first              </span>┃<span style="font-weight: bold"> last              </span>┃<span style="font-weight: bold"> frequency       </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime                    </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #800000; text-decoration-color: #800000">    2018-01-31    </span> │ <span style="color: #800000; text-decoration-color: #800000">   2101-04-30    </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">ME             </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime_no_freq            </span> │ <span style="color: #008080; text-decoration-color: #008080">    3</span> │ <span style="color: #008080; text-decoration-color: #008080">     0.3</span> │ <span style="color: #800000; text-decoration-color: #800000">    1992-01-05    </span> │ <span style="color: #800000; text-decoration-color: #800000">   2023-03-04    </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None           </span> │  │
│ └──────────────────────────────┴───────┴──────────┴────────────────────┴───────────────────┴─────────────────┘  │
│ <span style="font-style: italic">                                           &lt;class 'datetime.date'&gt;                                            </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column                           </span>┃<span style="font-weight: bold"> NA    </span>┃<span style="font-weight: bold"> NA %     </span>┃<span style="font-weight: bold"> first            </span>┃<span style="font-weight: bold"> last             </span>┃<span style="font-weight: bold"> frequency      </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date                   </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2018-01-31      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2101-04-30      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">ME            </span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date_no_freq           </span> │ <span style="color: #008080; text-decoration-color: #008080">    0</span> │ <span style="color: #008080; text-decoration-color: #008080">       0</span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">1992-01-05      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">2023-03-04      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">None          </span> │  │
│ └──────────────────────────────────┴───────┴──────────┴──────────────────┴──────────────────┴────────────────┘  │
│ <span style="font-style: italic">                                                 timedelta64                                                  </span>  │
│ ┏━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column         </span>┃<span style="font-weight: bold"> NA   </span>┃<span style="font-weight: bold"> NA %    </span>┃<span style="font-weight: bold"> mean                   </span>┃<span style="font-weight: bold"> median                 </span>┃<span style="font-weight: bold"> max                    </span>┃  │
│ ┡━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">time diff     </span> │ <span style="color: #008080; text-decoration-color: #008080">   5</span> │ <span style="color: #008080; text-decoration-color: #008080">    0.5</span> │ <span style="color: #008080; text-decoration-color: #008080">       8 days 00:05:47</span> │ <span style="color: #008080; text-decoration-color: #008080">       0 days 00:00:00</span> │ <span style="color: #008080; text-decoration-color: #008080">      26 days 00:00:00</span> │  │
│ └────────────────┴──────┴─────────┴────────────────────────┴────────────────────────┴────────────────────────┘  │
│ <span style="font-style: italic">                                                    string                                                    </span>  │
│ ┏━━━━━━━━┳━━━━┳━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold">        </span>┃<span style="font-weight: bold">    </span>┃<span style="font-weight: bold">      </span>┃<span style="font-weight: bold">            </span>┃<span style="font-weight: bold">           </span>┃<span style="font-weight: bold">            </span>┃<span style="font-weight: bold">           </span>┃<span style="font-weight: bold"> chars per  </span>┃<span style="font-weight: bold"> words per </span>┃<span style="font-weight: bold"> total      </span>┃  │
│ ┃<span style="font-weight: bold"> column </span>┃<span style="font-weight: bold"> NA </span>┃<span style="font-weight: bold"> NA % </span>┃<span style="font-weight: bold"> shortest   </span>┃<span style="font-weight: bold"> longest   </span>┃<span style="font-weight: bold"> min        </span>┃<span style="font-weight: bold"> max       </span>┃<span style="font-weight: bold"> row        </span>┃<span style="font-weight: bold"> row       </span>┃<span style="font-weight: bold"> words      </span>┃  │
│ ┡━━━━━━━━╇━━━━╇━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">text  </span> │ <span style="color: #008080; text-decoration-color: #008080"> 6</span> │ <span style="color: #008080; text-decoration-color: #008080"> 0.6</span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">How are   </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">Indeed,  </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">How are   </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">What     </span> │ <span style="color: #008080; text-decoration-color: #008080">      31.1</span> │ <span style="color: #008080; text-decoration-color: #008080">      5.8</span> │ <span style="color: #008080; text-decoration-color: #008080">      5761</span> │  │
│ │        │    │      │ <span style="color: #af87ff; text-decoration-color: #af87ff">you?      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">it was   </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">you?      </span> │ <span style="color: #af87ff; text-decoration-color: #af87ff">weather! </span> │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">the most </span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">outrageou</span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">sly      </span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">pompous  </span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">cat I    </span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">have ever</span> │            │           │            │           │            │  │
│ │        │    │      │            │ <span style="color: #af87ff; text-decoration-color: #af87ff">seen.    </span> │            │           │            │           │            │  │
│ └────────┴────┴──────┴────────────┴───────────┴────────────┴───────────┴────────────┴───────────┴────────────┘  │
│ <span style="font-style: italic">                                                    object                                                    </span>  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓  │
│ ┃<span style="font-weight: bold"> column                                                                  </span>┃<span style="font-weight: bold"> NA           </span>┃<span style="font-weight: bold"> NA %              </span>┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date                                                          </span> │ <span style="color: #008080; text-decoration-color: #008080">           0</span> │ <span style="color: #008080; text-decoration-color: #008080">                0</span> │  │
│ │ <span style="color: #af87ff; text-decoration-color: #af87ff">datetime.date_no_freq                                                  </span> │ <span style="color: #008080; text-decoration-color: #008080">           0</span> │ <span style="color: #008080; text-decoration-color: #008080">                0</span> │  │
│ └─────────────────────────────────────────────────────────────────────────┴──────────────┴───────────────────┘  │
╰────────────────────────────────────────────────────── End ──────────────────────────────────────────────────────╯
</pre>



It is recommended that you set your datatypes before using **skimpy** (for example converting any text columns to pandas string datatype), as this will produce richer statistical summaries. However, the `skim()` function will try and guess what the datatypes of your columns are.

## Requirements

You can find a full list of requirements in the [pyproject.toml](https://github.com/aeturrell/skimpy/blob/main/pyproject.toml) file.

You can try this package out right now in your browser using this
[Google Colab notebook](https://colab.research.google.com/gist/aeturrell/7bf183c559dc1d15ab7e7aaac39ea0ed/skimpy_demo.ipynb)
(requires a Google account). Note that the Google Colab notebook uses the latest package released on PyPI (rather than the development release).

## Installation

You can install the latest release of *skimpy* via
[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

```bash
$ pip install skimpy
```

To install the development version from git, use:

```bash
$ pip install git+https://github.com/aeturrell/skimpy.git
```

For development, see [contributing](contributing.qmd).

## License

Distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT), *skimpy* is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/aeturrell/skimpy/issues) along with a detailed description.

## Credits

This project was generated from [\@cjolowicz](https://github.com/cjolowicz)\'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.

**skimpy** was inspired by the R package [**skimr**](https://docs.ropensci.org/skimr/articles/skimr.html) and by exploratory Python packages including [**ydata_profiling**](https://docs.profiling.ydata.ai) and [**dataprep**](https://dataprep.ai/), from which the `clean_columns` function comes.

This package would not have been possible without the [**Rich**](https://github.com/Textualize/rich) package.

The package is built with [poetry](https://python-poetry.org/), while the documentation is built with [Quarto](https://quarto.org/) and [Quartodoc](https://github.com/machow/quartodoc) (a Python package). Tests are run with [nox](https://nox.thea.codes/en/stable/).

Using **skimpy** in your paper? Let us know by raising an issue beginning with "citation" and we'll add it to this page.
