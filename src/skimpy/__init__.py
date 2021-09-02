"""skimpy."""
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()
QUANTILES = [0, 0.25, 0.75]
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
    """[summary].

    Args:
        series (pd.Series): Numeric column of data frame for analysis

    Returns:
        dict: Mapping from series name to unicode histogram as list,
        eg '▃▅█'
    """
    hist, _ = np.histogram(series, density=True, bins=HIST_BINS)
    hist = hist / hist.max()
    # now do value counts
    key_vector = np.array(list(UNICODE_HIST.keys()), dtype="float")
    ucode_to_print = "".join(
        [UNICODE_HIST[find_nearest(key_vector, val)] for val in hist]
    )
    return pd.Series(index=[series.name], data=ucode_to_print)


def numeric_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame): Dataframe with columns of only numeric types

    Returns:
        pd.DataFrame: [description]
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
        xf (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
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


def text_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """[summary].

    Args:
        xf (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "<words/row>": pd.Series(
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


def skimpy(df: pd.DataFrame) -> None:
    """Skim a data frame and return statistics.

    skimpy() is an alternative to pandas.DataFrame.summary(), quickly providing
    an overview of a data frame. It produces a different set of summary
    functions based on the types of columns in the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to skim
    """
    if hasattr(df, "name"):
        name = df.name
    else:
        name = "dataframe"

    hyphen_break_length = 15
    tab_1_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
    console.print("─" * 10 + "[bold cyan]Data Summary[/bold cyan]" + "─" * 10)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column(name)
    table.add_column("Values")
    for key, val in tab_1_data.items():
        table.add_row(key, str(val))
    console.print(table)
    console.print("─" * hyphen_break_length)
    table_2 = Table(show_header=True, header_style="bold cyan")
    tab_2_data = df.dtypes.astype(str).value_counts().to_dict()
    table_2.add_column("Column Type")
    table_2.add_column("Count")
    for key, val in tab_2_data.items():
        table_2.add_row(key, str(val))
    console.print(table_2)
    console.print("─" * hyphen_break_length)
    if "category" in df.dtypes.astype(str).to_list():
        xf = pd.DataFrame(df.dtypes.astype(str))
        section_title = "Categorical Variables:" + " " * 10
        cat_names = list(xf[xf[0] == "category"].index)
        cat_var_string = (" " * len(section_title)).join([x + "\n" for x in cat_names])
        console.print(section_title + cat_var_string)
    types_to_select = ["number", "category", "datetime", "string"]
    for entry in types_to_select:
        xf = df.select_dtypes(entry)
        if not xf.empty:
            console.print(
                "── [bold cyan]Variable type:[/bold cyan] "
                + entry
                + "─" * hyphen_break_length
            )
            if entry == "number":
                num_df = numeric_variable_summary_table(xf)
                console.print(num_df.round(2))
            elif entry == "category":
                cat_df = category_variable_summary_table(xf)
                console.print(cat_df.round(2))
            elif entry == "string":
                txt_df = text_variable_summary_table(xf)
                console.print(txt_df.round(2))
