"""skimpy."""
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from rich.console import Console
from rich.table import Table

console = Console()
QUANTILES = [0, 0.25, 0.75, 1]
HIST_BINS = 6
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


def find_nearest(array: np.array, value: float) -> np.array:
    """[summary].

    Args:
        array (np.array): [description]
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
        xf (pd.DataFrame): [description]

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
        [create_unicode_hist(xf[col]) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    # reduce to 2 sf
    return summary_df


def variable_summary_table(df: pd.DataFrame, col_type: str) -> pd.DataFrame:
    """Produces a summary of all columns with one kind of dtype.

    Args:
        df: dataframe to summarise
        col_type: the pandas dtype of the columns to summarise

    Returns:
        summary_df: [description]
    """
    dtypes_df = df.dtypes.astype(str)
    columns = list(dtypes_df[dtypes_df == col_type].index)
    xf = df[columns]
    # if numeric
    if all([is_numeric_dtype(xf[col]) for col in xf.columns]):
        return numeric_variable_summary_table(xf)
    else:
        return pd.DataFrame()


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
    table_2.add_column("Frequency")
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
    for entry in df.dtypes.astype(str).to_list():
        if entry != "category":
            console.print(
                "── [bold cyan]Variable type:[/bold cyan] numeric"
                + "─" * hyphen_break_length
            )
            summ_df = variable_summary_table(df, "float64")
            console.print(summ_df.round(2))
