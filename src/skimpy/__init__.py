"""skimpy."""
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()


def variable_summary_table(df: pd.DataFrame, col_type: str) -> pd.DataFrame
    """[summary]

    Returns:
        summary_df: [description]
    """
    dtypes_df = df.dtypes.astype(str)
    columns = list(dtypes_df[dtypes_df == col_type].index)
    xf = df[columns]
    # if numeric
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "No. missing": count_nans_vec,
        "Complete rate": count_nans_vec/xf.shape[0],
        "mean": xf.mean(),
        "sd": xf.std(),
        }
    QUANTILES = [0, 0.25, 0.75, 1]
    quantiles_dict = dict(zip(["p" + str(int(x*100)) for x in QUANTILES],
                              [xf.quantile(x) for x in QUANTILES]))
    data_dict.update(quantiles_dict)
    # Create histogram using block elements
    # https://en.wikipedia.org/wiki/Block_Elements
    hist, _ = np.histogram(xf.iloc[:, 0], density=True, bins=10)
    hist = hist/hist.max()
    # now do value counts
    poss_values = [0, 1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8]

    summary_df = pd.DataFrame(data_dict)
    # reduce to 2 sf
    return summary_df


def skimpy(df: pd.DataFrame) -> None:
    """[summary]

    Args:
        df (pd.DataFrame): Dataframe to skim
    """
    try:
        name = df.name
    finally:
        name = "dataframe"

    hyphen_break_length = 15
    tab_1_data = {"Number of rows": df.shape[0],
                  "Number of columns": df.shape[1]}
    console.print("─"*10 + "[bold cyan]Data Summary[/bold cyan]" + "─"*10)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column(name)
    table.add_column("Values")
    for key, val in tab_1_data.items():
        table.add_row(
            key, str(val)
        )
    console.print(table)
    console.print("─"*hyphen_break_length)
    table_2 = Table(show_header=True, header_style="bold cyan")
    tab_2_data = df.dtypes.astype(str).value_counts().to_dict()
    table_2.add_column("Column Type")
    table_2.add_column("Frequency")
    for key, val in tab_2_data.items():
        table_2.add_row(
            key, str(val)
        )
    console.print(table_2)
    console.print("─"*hyphen_break_length)
    if('category' in df.dtypes.astype(str).to_list()):
        xf = pd.DataFrame(df.dtypes.astype(str))
        section_title = "Categorical Variables:" + " "*10
        cat_names = list(xf[xf[0] == "category"].index)
        cat_names = ["class", "cat"]
        cat_var_string = (" "*len(section_title)).join([x + "\n" for x in cat_names])
        console.print(section_title + cat_var_string)
    for entry in df.dtypes.astype(str).to_list():
        if entry!="category":
            console.print("── [bold cyan]Variable type:[/bold cyan] entry")

    console.print("▂▅▇")