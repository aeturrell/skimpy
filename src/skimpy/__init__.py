"""skimpy."""
import numpy as np
import pandas as pd
import rich
from collections import defaultdict
from numpy.random import Generator
from numpy.random import PCG64
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()
QUANTILES = [0, 0.25, 0.75, 1]
HIST_BINS = 5
UNICODE_HIST = {
    0: " ",
    1 / 8: "▁",
    1 / 4: "▂",
    3 / 8: "▃",
    1 / 2: "▄",
    5 / 8: "▅",
    3 / 4: "▆",
    7 / 8: "▇",
    1: "█",
}


def dataframe_to_rich_table(
    table_name: str,
    df: pd.DataFrame,
    row_limit: int = 20,
    col_limit: int = 10,
    str_limit: int = 20,
) -> rich.table.Table:
    """[summary].

    Args:
        table_name (str): [description]
        df (pd.DataFrame): [description]
        row_limit (int): [description]. Defaults to 20.
        col_limit (int): [description]. Defaults to 10.
        str_limit (int): [description]. Defaults to 20.

    Returns:
        rich.table.Table: [description]
    """
    df = df.reset_index().rename(columns={"index": ""})
    table = Table(show_footer=False, expand=True, title=table_name, show_header=True)
    datatype_colours = {
        "number": "cyan",
        "category": "magenta",
        "datetime": "red",
        "string": "green",
        "bool": "turquoise2",
        "object": "medium_purple1",
    }
    cols_to_cat_map = dict(
        zip(
            datatype_colours.keys(),
            [
                list(df.select_dtypes(entry).columns)
                for entry in datatype_colours.keys()
            ],
        )
    )
    type_by_col = defaultdict(list)
    for k, seq in cols_to_cat_map.items():
        for letter in seq:
            type_by_col[letter].append(k)
    type_by_col = dict(zip(type_by_col.keys(), [x[0] for x in type_by_col.values()]))
    type_to_colour = dict(
        zip(type_by_col.keys(), [datatype_colours[x] for x in type_by_col.values()])
    )
    columns = list(df.columns[:col_limit])
    col_pos_to_colour = dict(
        zip(range(len(columns)), [type_to_colour[x] for x in columns])
    )
    rows = df.values[:row_limit]
    for col in columns:
        table.add_column(str(col), no_wrap=True)
    for row in rows:
        row = row[:col_limit]
        row = [
            Text(str(item)[:str_limit], style=col_pos_to_colour[i])
            for i, item in enumerate(row)
        ]
        table.add_row(*list(row))
    return table


def find_nearest(array, value):
    """[summary].

    Args:
        array (np.ndarray): [description]
        value (float): [description]

    Returns:
        np.array: [description]
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def create_unicode_hist(series: pd.Series) -> pd.Series:
    """Return a histogram rendered in unicode.

    Given a pandas series of numerical values, returns a series with one
    entry, the original series name, and a histogram made up of unicode
    characters.

    Args:
        series (pd.Series): Numeric column of data frame for analysis

    Returns:
        pd.Series: Index of series name and entry with unicode histogram as
        a string, eg '▃▅█'
    """
    hist, _ = np.histogram(series, density=True, bins=HIST_BINS)
    hist = hist / hist.max()
    # now do value counts
    key_vector = np.array(list(UNICODE_HIST.keys()), dtype="float")
    ucode_to_print = "".join(
        [UNICODE_HIST[find_nearest(key_vector, val)] for val in hist]
    )
    return pd.Series(index=[series.name], data=ucode_to_print, dtype="string")


def numeric_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame): Dataframe with columns of only numeric types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "mean": xf.mean(),
        "sd": xf.std(),
    }
    display_quantiles_as_pct = 100
    quantiles_dict = dict(
        zip(
            ["p" + str(int(x * display_quantiles_as_pct)) for x in QUANTILES],
            [xf.quantile(x) for x in QUANTILES],
        )
    )
    data_dict.update(quantiles_dict)
    # Create histogram using unicode block elements
    # https://en.wikipedia.org/wiki/Block_Elements
    hist_series = pd.concat(
        [create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


def category_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "ordered": pd.Series(
            dict(zip(xf.columns, [xf[col].cat.ordered for col in xf.columns]))
        ),
        "unique": pd.Series(
            dict(zip(xf.columns, [len(xf[col].unique()) for col in xf.columns]))
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


def bool_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_trues = xf.sum()
    data_dict = {
        "true": xf.sum(),
        "true rate": xf.sum() / xf.shape[0],
    }
    hist_series = pd.concat(
        [create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


def string_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only string types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "words per row": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf[col].str.len().sum() / len(xf) for col in xf.columns],
                )
            )
        ),
        "total words": pd.Series(
            dict(zip(xf.columns, [xf[col].str.len().sum() for col in xf.columns]))
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


def datetime_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Provides summaries of dataframes containing datetime columns.

    Args:
        xf (pd.DataFrame): A dataframe with only datetime columns

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "first": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf[col].min() for col in xf.columns],
                )
            )
        ),
        "last": pd.Series(dict(zip(xf.columns, [xf[col].max() for col in xf.columns]))),
    }
    if len(xf) > 3:
        data_dict.update(
            {
                "frequency": pd.Series(
                    dict(
                        zip(xf.columns, [pd.infer_freq(xf[col]) for col in xf.columns])
                    )
                )
            }
        )
    summary_df = pd.DataFrame(data_dict)
    return summary_df


def skimpy(df: pd.DataFrame) -> None:
    """Skim a data frame and return statistics.

    skimpy is an alternative to pandas.DataFrame.summary(), quickly providing
    an overview of a data frame. It produces a different set of summary
    functions based on the types of columns in the dataframe. You may get
    better results from ensuring that you set the datatypes you want before
    running skimpy.

    Args:
        df (pd.DataFrame): Dataframe to skim
    """
    if hasattr(df, "name"):
        # Catch this edge case
        if("name" in df.columns):
            name = "dataframe"
        else:
            name = df.name
    else:
        name = "dataframe"

    # Data summary
    tab_1_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
    dat_sum_table = Table(
        title="Data Summary", show_header=True, header_style="bold cyan"
    )
    dat_sum_table.add_column(name)
    dat_sum_table.add_column("Values")
    for key, val in tab_1_data.items():
        dat_sum_table.add_row(key, str(val))
    # Data tpes
    types_sum_table = Table(
        title="Data Types", show_header=True, header_style="bold cyan"
    )
    tab_2_data = df.dtypes.astype(str).value_counts().to_dict()
    types_sum_table.add_column("Column Type")
    types_sum_table.add_column("Count")
    for key, val in tab_2_data.items():
        types_sum_table.add_row(key, str(val))
    # Categorys
    if "category" in df.dtypes.astype(str).to_list():
        xf = pd.DataFrame(df.dtypes.astype(str))
        cat_sum_table = Table()
        cat_sum_table.add_column("[bold cyan]Categorical Variables[/bold cyan]")
        cat_names = list(xf[xf[0] == "category"].index)
        for cat in cat_names:
            cat_sum_table.add_row(cat)
    # Summaries of cols of specific types
    types_funcs_dict = {
        "number": numeric_variable_summary_table,
        "category": category_variable_summary_table,
        "datetime": datetime_variable_summary_table,
        "string": string_variable_summary_table,
        "bool": bool_variable_summary_table,
    }
    list_of_tabs = []
    for col_type, summary_func in types_funcs_dict.items():
        xf = df.select_dtypes(col_type)
        if not xf.empty:
            sum_df = summary_func(xf)
            list_of_tabs.append(dataframe_to_rich_table(col_type, sum_df.round(2)))
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_row(dat_sum_table)
    grid.add_row(types_sum_table)
    if "category" in df.dtypes.astype(str).to_list():
        grid.add_row(cat_sum_table)
    for sum_tab in list_of_tabs:
        grid.add_row(sum_tab)
    console.print(Panel.fit(grid))


def generate_test_data() -> pd.DataFrame:
    """Generate dataframe with several different datatypes.

    Returns:
        pd.DataFrame: dataframe with columns spanning several data types.
    """
    seed = 34729
    rng = Generator(PCG64(seed))
    columns_df = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
    df = pd.DataFrame(
        [
            [0, 3.5, 1.4, 0.2, "setosa"],
            [0, 3, 1.4, 0.2, "setosa"],
            [0, 3.2, 1.3, 0.2, "setosa"],
            [1, 3.1, 1.5, 0.2, "setosa"],
            [1, 3.6, 1.4, 0.2, "setosa"],
            [2, 3.9, 1.7, 0.4, "setosa"],
            [3, np.nan, 1.4, 0.3, "setosa"],
            [2, 3.4, 1.5, 0.2, "virginica"],
            [1, 2.9, 1.4, 0.2, "virginica"],
            [1, 3.1, 1.5, 0.1, "virginica"],
            [0, 3.7, 1.5, 0.2, "virginica"],
            [0, 3.4, 1.6, 0.2, "virginica"],
            [0, 3, 1.4, 0.1, "virginica"],
        ],
        columns=columns_df,
    )
    df["rand_flower"] = rng.normal(size=(len(df)), scale=0.1, loc=0)
    second_cat_var_entries = ["UK", "Mexico", "USA", "India"]
    df["location"] = rng.choice(second_cat_var_entries, len(df))
    df["location"] = df["location"].astype("category")
    df.loc[3, "location"] = np.nan
    df["class"] = df["class"].astype("category")
    df["booly_col"] = rng.choice([True, False], size=(len(df)))
    df["booly_col"] = df["booly_col"].astype(bool)
    # string column
    string_options = [
        "How are you?",
        "What weather!",
        "Indeed, it was the most outrageously pompous cat I have ever seen.",
    ]
    df["text"] = rng.choice(string_options, len(df))
    df.loc[[3, 5, 8, 9], "text"] = None
    df["text"] = df["text"].astype("string")
    # add a datetime column
    df["date"] = pd.date_range("2018-01-01", periods=len(df), freq="M")
    df["date_no_freq"] = rng.choice(
        (pd.to_datetime(pd.Series(["01/01/2022", "03/04/2023", "01/05/1992"]))), len(df)
    )
    df.loc[3, "date_no_freq"] = pd.NaT
    return df
