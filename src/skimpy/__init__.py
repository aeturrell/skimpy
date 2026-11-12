"""skimpy provides summary statistics about variables in pandas data frames."""

from __future__ import annotations

import datetime as dt
import os
import re
import typing
import warnings
from collections import defaultdict
from itertools import chain
from typing import Any
from unicodedata import normalize

import numpy as np
import pandas as pd
import pyarrow as pa
from numpy.random import PCG64, Generator
from rich.columns import Columns
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typeguard import typechecked

# polars check
try:
    import polars as pl
except ImportError:
    # no nothing
    pass

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("skimpy")
except PackageNotFoundError:
    __version__ = "unknown"

NULL_VALUES = {np.nan, "", None}

CASE_STYLES = {
    "snake",
    "kebab",
    "camel",
    "pascal",
    "const",
    "sentence",
    "title",
    "lower",
    "upper",
}

QUANTILES = [0, 0.25, 0.5, 0.75, 1]
HIST_BINS = 6
# These are defined globally because they are used in more than one function
DATE_COL_FIRST = "first"
DATE_COL_LAST = "last"
NUM_COL_MEAN = "mean"
COMPLETE_COL = "NA %"
MISSING_COL = "NA"
# Shown in place of a frequency when none can be inferred
NO_FREQUENCY = "NA"

UNSUPPORTED_INFERRED_TYPES = [
    "mixed-integer",
    "mixed",
    "mixed-integer-float",
    "unknown-array",
]

type JSON = dict[str, dict[str, Any]]

# pd.api.types.infer_dtype result -> dtype that column is cast to
_INFERRED_TO_DTYPE: dict[str, Any] = {
    "string": "string",
    "integer": "int",
    "floating": "float64",
    "decimal": "float64",
    "categorical": "category",
    "boolean": "bool",
    "complex": "complex128",
    # Entirely null columns, which will be dealt with later
    "empty": "object",
    # pandas has no numpy date dtype: Python dates sit in "object" columns.
    # Give them a real date dtype so they can be routed precisely, rather
    # than being lumped in with other objects.
    "date": "date32[pyarrow]",
}
# Inferred types that are datetimes / timedeltas. These keep their existing
# resolution (unit), as forcing nanoseconds overflows outside c. 1677-2262 for
# datetimes, and beyond c. 292 years for timedeltas.
_INFERRED_DATETIMES = {"datetime64", "datetime"}
_INFERRED_TIMEDELTAS = {"timedelta64", "timedelta"}


def _strip_tzinfo(value: Any) -> Any:
    """Drop the timezone of a datetime, keeping its wall time.

    Args:
        value (Any): A single entry of a column, eg a datetime.datetime.

    Returns:
        Any: The value, made timezone-naive if it was a timezone-aware datetime.
    """
    if isinstance(value, dt.datetime) and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


def _to_naive_datetime64(series: pd.Series) -> pd.Series:
    """Convert a datetime-like column to timezone-naive datetime64.

    A column that is already datetime64 keeps its unit. A column of datetime
    objects is converted at a resolution pandas can hold its range in.

    Args:
        series (pd.Series): Column of datetime64 type or of datetime objects.

    Returns:
        pd.Series: Column of timezone-naive datetime64 type.
    """
    if isinstance(series.dtype, pd.DatetimeTZDtype):
        return series.dt.tz_localize(None)
    if pd.api.types.is_datetime64_dtype(series.dtype):
        return series
    # Datetime objects: drop timezones element-wise, which (unlike pandas'
    # conversions) also works when the objects have a mix of timezones.
    series = series.map(_strip_tzinfo, na_action="ignore")
    try:
        return pd.to_datetime(series)
    except pd.errors.OutOfBoundsDatetime:
        # pandas < 3 converts objects to nanoseconds only. Python datetimes
        # have microsecond resolution, so this is lossless.
        return series.astype("datetime64[us]")


def _to_timedelta64(series: pd.Series) -> pd.Series:
    """Convert a timedelta-like column to timedelta64.

    A column that is already timedelta64 keeps its unit.

    Args:
        series (pd.Series): Column of timedelta64 type or of timedelta objects.

    Returns:
        pd.Series: Column of timedelta64 type.
    """
    if pd.api.types.is_timedelta64_dtype(series.dtype):
        return series
    try:
        return pd.to_timedelta(series)
    except pd.errors.OutOfBoundsTimedelta:
        # pandas < 3 converts objects to nanoseconds only. Python timedeltas
        # have microsecond resolution, so this is lossless.
        values = np.array(series.to_numpy(), dtype="timedelta64[us]")
        return pd.Series(values, index=series.index, name=series.name)


@typechecked
def _infer_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """Infers the, and applies new, datatypes of dataframe columns.

    Columns whose inferred type has no better dtype to cast to (eg bytes,
    datetime.time, period, interval) are left as they are. Datetime and
    timedelta columns keep their existing resolution.

    Args:
        df (pd.DataFrame): User data that we'd like to infer types on.

    Returns:
        pd.DataFrame: Same dataframe, but typed wherever possible.
    """
    inferred_types = df.apply(pd.api.types.infer_dtype, axis=0)
    for column, inferred in inferred_types.items():
        if inferred in _INFERRED_DATETIMES:
            df[column] = _to_naive_datetime64(df[column])
        elif inferred in _INFERRED_TIMEDELTAS:
            df[column] = _to_timedelta64(df[column])
        elif inferred in _INFERRED_TO_DTYPE:
            df[column] = df[column].astype(_INFERRED_TO_DTYPE[inferred])
    return df


def _na_percent(count_nans: pd.Series, n_rows: int) -> pd.Series:
    """Percentage of entries that are missing, rounded to 2 decimal places.

    Args:
        count_nans (pd.Series): Number of missing entries in each column.
        n_rows (int): Number of rows in the dataframe.

    Returns:
        pd.Series: Percentage missing in each column.
    """
    return (100 * count_nans / n_rows).round(2)


@typechecked
def _round_series(s: pd.Series, places: int = 2) -> pd.Series:
    """Rounds numerical series to places number of significant figures

    Args:
        s (pd.Series): Input series
        places (int, optional): Number of significant figures to round to. Defaults to 2.

    Returns:
        pd.Series: Series with numbers rounded to places s.f.
    """
    s = s.apply(lambda x: float(f"{float(f'{x:.{places}g}'):g}"))
    return s


@typechecked
def _map_row_positions_to_text_style(types_to_property: dict, df: pd.DataFrame) -> dict:
    """Maps positions in summary dataframe (eg row) to a Rich text property.

    Args:
        types_to_property (dict): _description_
        df (pd.DataFrame):  Dataframe to map positions in

    Returns:
        dict: Dictionary mapping row position to Rich text property
    """
    # Sections without their own style share that of the closest broad type
    section_to_style_group = {"timedelta64[ns]": "number", "date": "datetime"}
    row_pos_to_property = {}
    for pos, dtype in enumerate(df.dtypes):
        section = _section_for_dtype(dtype)
        group = section_to_style_group.get(section, section)
        row_pos_to_property[pos] = types_to_property.get(
            group, types_to_property["object"]
        )
    return row_pos_to_property


@typechecked
def _simplify_datetimes_in_array(rows: np.ndarray) -> np.ndarray:
    """Simplifies 2001/01/01 00:00:00 to 2001/01/01.

    Args:
        rows (np.ndarray):  contain summary info, including datetimes

    Returns:
        np.ndarray: rows with any all zero hours/min/sec stripped out
    """
    timestamp_positions = [
        [[idx, i] for i, j in enumerate(item) if isinstance(j, pd.Timestamp)]
        for idx, item in enumerate(rows)
    ]
    timestamp_pos_list = list(chain.from_iterable(timestamp_positions))
    timestamp_pos_tuples = [tuple(entry) for entry in timestamp_pos_list]
    for entry in timestamp_pos_tuples:
        hour, min, sec = rows[entry].hour, rows[entry].minute, rows[entry].second
        if hour == min == sec == 0:
            rows[entry] = rows[entry].strftime("%Y-%m-%d")
    return rows


MIN_COL_WIDTH: int = 6
MAX_COL_WIDTH: int = 40


def _compute_column_widths(df: pd.DataFrame) -> list[int]:
    """Compute appropriate max_width for each column based on content.

    Examines header length and the longest value in each column, then
    clamps to [MIN_COL_WIDTH, MAX_COL_WIDTH].

    Args:
        df (pd.DataFrame): The dataframe whose columns to measure.

    Returns:
        list[int]: A max_width value for each column.
    """
    widths = []
    for col in df.columns:
        header_width = len(str(col))
        content_width = max((len(str(v)) for v in df[col]), default=0)
        ideal = max(header_width, content_width)
        clamped = max(MIN_COL_WIDTH, min(MAX_COL_WIDTH, ideal))
        widths.append(clamped)
    return widths


@typechecked
def _dataframe_to_rich_table(
    table_name: str,
    df: pd.DataFrame,
    number: str = "cyan",
    category: str = "magenta",
    datetime: str = "red",
    string: str = "green",
    bool: str = "turquoise2",
    object: str = "medium_purple1",
) -> Table:
    """Converts a dataframe into a rich table.

    To pretty print a dataframe to the console or interactive console, it needs
    to first be converted into a rich table. This function performs that
    conversion and also colours entries in tables depending on their broad
    datatype. This function processes summaries (themselves dataframes) and is
    used to produce a table for each data type in the dataframe to be skimmed.
    A list of standard colours may be found at
    https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors

    Args:
        table_name (str): Usually one of 'number', 'bool', etc. Used as title.
        df (pd.DataFrame): summary of all data of one datatype
        number (str): colour to render numbers in
        category (str): colour to render categories in
        datetime (str): colour to render datetimes in
        string (str): colour to render strings in
        bool (str): colour to render bools in
        object (str): colour to render objects in

    Returns:
        Table: instance of Table from the rich package
    """
    df = df.reset_index().rename(columns={"index": "column"})
    table = Table(
        show_footer=False, expand=True, title=escape(table_name), show_header=True
    )
    # generate dict of types to colours
    datatype_colours = {
        "number": number,
        "category": category,
        "datetime": datetime,
        "string": string,
        "bool": bool,
        "object": object,
    }
    # generate dict of types to text justifications
    datatype_justify = {
        "number": "right",
        "category": "center",
        "datetime": "center",
        "string": "center",
        "bool": "left",
        "object": "left",
    }
    pos_to_colour = _map_row_positions_to_text_style(datatype_colours, df)
    pos_to_justification = _map_row_positions_to_text_style(datatype_justify, df)
    rows = df.values
    # find any datetimes
    if DATE_COL_FIRST in df.columns or DATE_COL_LAST in df.columns:
        rows = _simplify_datetimes_in_array(rows)
    rows_list_list = [
        [str(s).rstrip("0").rstrip(".") if isinstance(s, float) else s for s in row]
        for row in rows
    ]
    col_widths = _compute_column_widths(df)
    for col, width in zip(df.columns, col_widths):
        table.add_column(escape(str(col)), overflow="fold", max_width=width)
    for row in rows_list_list:
        row = [
            Text(
                str(item),
                style=pos_to_colour[i],
                justify=pos_to_justification[i],
            )
            for i, item in enumerate(row)
        ]
        table.add_row(*list(row))
    return table


def _find_nearest(array: np.ndarray, value: float) -> float:
    """Find the nearest numerical match to value in an array.

    Args:
        array (np.ndarray): An array of numbers to match with.
        value (float): Single value to find an entry in array that is close.

    Returns:
        float: The entry in array that is closest to value.
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


@typing.no_type_check
def _create_unicode_hist(series: pd.Series) -> pd.Series:
    """Return a histogram rendered in block unicode.

    Given a pandas series of numerical values, returns a series with one
    entry, the original series name, and a histogram made up of unicode
    characters. However, note that the histogram is very approximate, partly
    due to limitations in how unicode is displayed across systems.

    Args:
        series (pd.Series): Numeric column of data frame for analysis

    Returns:
        pd.Series: Index of series name and entry with unicode histogram as
        a string, eg '▃▅█'
    """
    if series.dtype == "bool":
        series = series.astype("int")
    hist, _ = np.histogram(series, density=True, bins=HIST_BINS)
    hist = hist / hist.max()
    fractions = [
        0.0,
        1 / 8,
        1 / 4,
        3 / 8,
        1 / 2,
        5 / 8,
        3 / 4,
        7 / 8,
        1.0,
    ]
    # add in empty string
    unicode_hist = {fractions[0]: " "}
    # Unicode block elements for bar characters
    unicode_hist.update(
        {key: chr(code) for key, code in zip(fractions[1:], range(0x2581, 0x2589))}
    )
    # NB: unicode 1/2 and 8/8 blocks have inconsistent widths depending on font
    # systems, so, to make skimpy work on all systems, hist blocks are pinned to
    # nearest available consistent width block for Windows.
    # Remove specific bar characters if on Windows
    if os.name != "posix":
        del unicode_hist[1 / 2]
        del unicode_hist[1.0]

    key_vector = np.array(list(unicode_hist.keys()), dtype="float")
    ucode_to_print = "".join(
        [unicode_hist[_find_nearest(key_vector, val)] for val in hist]
    )
    return pd.Series(index=[series.name], data=ucode_to_print, dtype="string")


@typechecked
def _numeric_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have numeric type.
    WARNING: this usually rounds to 4 significant figures.

    Args:
        xf (pd.DataFrame): Dataframe with columns of only numeric types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        NUM_COL_MEAN: _round_series(xf.mean(), 4),
        "sd": _round_series(xf.std(), 4),
    }
    display_quantiles_as_pct = 100
    quantiles_dict = dict(
        zip(
            ["p" + str(int(x * display_quantiles_as_pct)) for x in QUANTILES],
            [_round_series(xf.quantile(x), 4) for x in QUANTILES],
        )
    )
    data_dict.update(quantiles_dict)
    # Create histogram using unicode block elements
    # https://en.wikipedia.org/wiki/Block_Elements
    hist_series = pd.concat(
        [_create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _category_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have category type.

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        "ordered": pd.Series(
            dict(zip(xf.columns, [xf[col].cat.ordered for col in xf.columns]))
        ),
        "unique": pd.Series(
            dict(zip(xf.columns, [len(xf[col].unique()) for col in xf.columns]))
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _bool_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have boolean type.

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    data_dict = {
        "true": xf.sum(),
        "true rate": _round_series(xf.sum() / xf.shape[0]),
    }
    hist_series = pd.concat(
        [_create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _string_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have string type. (NB not object type).

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only string types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        "shortest": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf.loc[xf[col].str.len().idxmin(), col] for col in xf.columns],  # type: ignore
                )
            )
        ),
        "longest": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf.loc[xf[col].str.len().idxmax(), col] for col in xf.columns],  # type: ignore
                )
            )
        ),
        # Below are alphabetical min and max
        "min": pd.Series(
            dict(zip(xf.columns, [xf[col].sort_values().iloc[0] for col in xf.columns]))
        ),
        "max": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [
                        xf[col].sort_values(ascending=False).iloc[0]
                        for col in xf.columns
                    ],
                )
            )
        ),
        "chars per row": _round_series(
            pd.Series(
                dict(zip(xf.columns, [xf[col].str.len().mean() for col in xf.columns]))
            ),
            3,
        ),
        "words per row": _round_series(
            pd.Series(
                dict(
                    zip(
                        xf.columns,
                        [
                            xf[col].str.count(" ").add(1).sum() / len(xf)
                            for col in xf.columns
                        ],
                    )
                )
            )
        ),
        "total words": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf[col].str.count(" ").add(1).sum() for col in xf.columns],
                )
            ),
            dtype="int",
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _timedelta_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have timedelta type. (NB not object type).

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only timedelta types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    # NB: timedelta doesn't play nicely with rounding
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        NUM_COL_MEAN: xf.mean().dt.floor("s"),
        "median": xf.median().dt.floor("s"),
        "max": xf.max().dt.ceil("s"),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


# pandas 3.1 deprecated infer_freq returning a string; this option opts in to
# the future behaviour (returning an offset). It doesn't exist in older pandas.
try:
    pd.get_option("future.infer_freq_returns_offset")
    _INFER_FREQ_OFFSET_OPTION: bool = True
except pd.errors.OptionError:
    _INFER_FREQ_OFFSET_OPTION = False


def _infer_freq_str(series: pd.Series) -> str | None:
    """Infer the frequency of a datetime series as a string, eg "D" or "ME".

    Args:
        series (pd.Series): A series of datetime64 type.

    Returns:
        str | None: The frequency string, or None if no frequency could be inferred.
    """
    if _INFER_FREQ_OFFSET_OPTION:
        with pd.option_context("future.infer_freq_returns_offset", True):
            freq = pd.infer_freq(series)
    else:
        freq = pd.infer_freq(series)
    if freq is None or isinstance(freq, str):
        return freq
    return freq.freqstr


def _is_date_dtype(dtype: Any) -> bool:
    """Whether a dtype holds calendar dates (without times), eg date32[pyarrow].

    Args:
        dtype (Any): A pandas or numpy dtype.

    Returns:
        bool: True if the dtype is a pyarrow date type.
    """
    return isinstance(dtype, pd.ArrowDtype) and pa.types.is_date(dtype.pyarrow_dtype)


def _section_for_dtype(dtype: Any) -> str:
    """Assign a column's dtype to exactly one summary section.

    Order matters: more specific types are checked before the broader types
    that also match them (eg bool and dates before numbers). Any dtype without
    a dedicated summary (eg bytes, period, interval) falls back to the "object"
    section, which reports missing values only, so no column is ever dropped.

    Args:
        dtype (Any): A (post-inference) column dtype.

    Returns:
        str: Name of the summary section.
    """
    if _is_date_dtype(dtype):
        return "date"
    if pd.api.types.is_bool_dtype(dtype):
        return "bool"
    if isinstance(dtype, pd.CategoricalDtype):
        return "category"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    if pd.api.types.is_timedelta64_dtype(dtype):
        return "timedelta64[ns]"
    if pd.api.types.is_object_dtype(dtype):
        return "object"
    if pd.api.types.is_string_dtype(dtype):
        return "string"
    if pd.api.types.is_numeric_dtype(dtype):
        return "number"
    return "object"


@typechecked
def _datetime_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have datetime type.

    Args:
        xf (pd.DataFrame): A dataframe with only datetime columns

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        DATE_COL_FIRST: pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf[col].min() for col in xf.columns],
                )
            )
        ),
        DATE_COL_LAST: pd.Series(
            dict(zip(xf.columns, [xf[col].max() for col in xf.columns]))
        ),
    }
    if len(xf) > 3:
        data_dict.update(
            {
                "frequency": pd.Series(
                    dict(
                        zip(
                            xf.columns,
                            [
                                _infer_freq_str(xf[col]) or NO_FREQUENCY
                                for col in xf.columns
                            ],
                        )
                    )
                )
            }
        )
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _date_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have date (no time) type.

    First and last are reported as datetime.date; frequency inference is done
    on a datetime64 view of the column, as pandas cannot infer it on dates.

    Args:
        xf (pd.DataFrame): A dataframe with only date columns

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
        DATE_COL_FIRST: pd.Series({col: xf[col].min() for col in xf.columns}),
        DATE_COL_LAST: pd.Series({col: xf[col].max() for col in xf.columns}),
    }
    if len(xf) > 3:
        data_dict.update(
            {
                "frequency": pd.Series(
                    {
                        col: _infer_freq_str(pd.to_datetime(xf[col])) or NO_FREQUENCY
                        for col in xf.columns
                    }
                )
            }
        )
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _empty_column_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have all empty entries.

    Args:
        xf (pd.DataFrame): A dataframe with only empty columns

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        MISSING_COL: count_nans_vec,
        COMPLETE_COL: _na_percent(count_nans_vec, xf.shape[0]),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def _delete_unsupported_columns(df: pd.DataFrame) -> pd.DataFrame:
    """This will remove the pd.api.types.infer_dtype types that are not
    supported.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        pd.DataFrame: Dataframe with unsupported columns removed.

    Raises:
        ValueError: If the input dataframe only has unsupported column types.
    """
    df_types = (
        pd.DataFrame(df.apply(pd.api.types.infer_dtype, axis=0))
        .reset_index()
        .rename(columns={"index": "column", 0: "type"})
    )
    df_types["delete"] = df_types["type"].isin(UNSUPPORTED_INFERRED_TYPES)
    for _, row in df_types.iterrows():
        if row["delete"]:
            df = df.drop(row["column"], axis=1)
    if df.empty:
        raise ValueError(
            f"Your input dataframe only has unsupported column types, eg {', '.join(UNSUPPORTED_INFERRED_TYPES)}"
        )
    return df


@typechecked
def _skim_computation(
    df_in: pd.DataFrame,
) -> tuple[Table, JSON]:
    """Performs the under-the-hood summary statistics.

    Args:
        df_in (pd.DataFrame): Input pandas dataframe to create a summary of.

    Returns:
        tuple[Table, JSON]: Rich table grid to print to console, JSON of summary stats.
    """
    if hasattr(df_in, "name") and "name" not in df_in.columns:
        name = str(df_in.name)
    else:
        name = "Dataframe"

    # Make a copy so as not to mess with dataframe
    df = df_in.copy()
    # remove any columns with types that are not currently supported
    df = _delete_unsupported_columns(df)
    # Perform inference of datatypes
    df = _infer_datatypes(df)

    header_style = "bold cyan"  # fixed
    # main data dict
    json_data: Any = {}
    # Data summary
    tab_1_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
    dat_sum_table_title = "Data Summary"
    dat_sum_table = Table(
        title=dat_sum_table_title, show_header=True, header_style=header_style
    )
    dat_sum_table.add_column(escape(name))
    dat_sum_table.add_column("Values")
    for key, val in tab_1_data.items():
        dat_sum_table.add_row(key, str(val))
    json_data.update({dat_sum_table_title: tab_1_data})
    # Data types
    data_types_title = "Data Types"
    types_sum_table = Table(
        title=data_types_title, show_header=True, header_style=header_style
    )
    tab_2_data = df.dtypes.astype(str).value_counts().to_dict()
    types_sum_table.add_column("Column Type")
    types_sum_table.add_column("Count")
    for key, val in tab_2_data.items():
        types_sum_table.add_row(escape(str(key)), str(val))
    json_data.update({data_types_title: tab_2_data})
    # Categorys
    if "category" in df.dtypes.astype(str).to_list():
        cat_section_title = "Categories"
        xf = pd.DataFrame(df.dtypes.astype(str))
        cat_sum_table = Table(
            title=cat_section_title, show_header=True, header_style=header_style
        )
        header_string = f"[{header_style}]Categorical Variables[/{header_style}]"
        cat_sum_table.add_column(header_string)
        cat_names = list(xf[xf[0] == "category"].index)
        for cat in cat_names:
            cat_sum_table.add_row(escape(str(cat)))
        json_data.update(
            {cat_section_title: {"Columns": {cat_name for cat_name in cat_names}}}
        )
    # Summaries of cols of specific types
    # Section name -> summary function; sections are printed in this order
    types_funcs_dict = {
        "number": _numeric_variable_summary_table,
        "category": _category_variable_summary_table,
        "bool": _bool_variable_summary_table,
        "datetime": _datetime_variable_summary_table,
        "date": _date_variable_summary_table,
        "timedelta64[ns]": _timedelta_variable_summary_table,
        "string": _string_variable_summary_table,
        "object": _empty_column_summary_table,
    }
    list_of_tabs = []
    # We now need a special approach to deal with columns that are just null
    xf = df.loc[:, df.isnull().all()]
    if not xf.empty:
        sum_df = _empty_column_summary_table(xf)
        col_type_to_rich = "All null"
        list_of_tabs.append(_dataframe_to_rich_table(col_type_to_rich, sum_df))
        json_data.update({col_type_to_rich: sum_df.to_dict()})
    # remove all null columns as already dealt with
    # and other variables have "object" type too.
    df = df.loc[:, ~df.isnull().all()].copy()
    # Route each column to exactly one section based on its dtype
    sections = [_section_for_dtype(dtype) for dtype in df.dtypes]
    for section, summary_func in types_funcs_dict.items():
        xf = df.loc[:, [s == section for s in sections]]
        if not xf.empty:
            sum_df = summary_func(xf)
            list_of_tabs.append(_dataframe_to_rich_table(section, sum_df))
            json_data.update({section: sum_df.to_dict()})

    # Put all of the info together
    grid = Table.grid(expand=True)
    tables_list = [dat_sum_table, types_sum_table]
    if "category" in df.dtypes.astype(str).to_list():
        tables_list.append(cat_sum_table)
    grid.add_row(Columns(tables_list))
    grid.add_column(justify="left")
    for sum_tab in list_of_tabs:
        grid.add_row(sum_tab)
    # Weirdly, iteration over list of tabs misses last entry
    grid.add_row(list_of_tabs[-1])
    return grid, json_data


@typechecked
def skim(
    df_in: pd.DataFrame | pl.DataFrame,
) -> None:
    """Skim a pandas or polars dataframe and return visual summary statistics on it.

    skim is an alternative to pandas.DataFrame.describe(), quickly providing
    an overview of a data frame via a table displayed in the console. It produces a different set of summary
    functions based on the types of columns in the dataframe. You may get
    better results from ensuring that you set the datatypes in your dataframe
    you want before running skim.

    Note that any unknown column types, or mixed column types, will not be
    processed.

    Args:
        df_in (pd.DataFrame | pl.DataFrame): Dataframe to skim.

    Raises:
        NotImplementedError: If the dataframe has a MultiIndex column structure.

    Examples:
        Skim a dataframe

        >>> df = pd.DataFrame(
                {
                'col1': ['Philip', 'Turanga', 'bob'],
                'col2': [50, 100, 70],
                'col3': [False, True, True]
                })
        >>> df["col1"] = df["col1"].astype("string")
        >>> skim(df)
    """
    if isinstance(df_in.columns, pd.MultiIndex):
        raise NotImplementedError(
            "Skimpy does not currently support multi-column indexes. Try using a simple column structure."
        )

    df_out = _convert_to_pandas(df_in)
    grid, _ = _skim_computation(df_out)
    console = Console(record=True)
    console.print(Panel(grid, title="skimpy summary", subtitle="End"))


def _convert_to_pandas(df_in: pd.DataFrame | pl.DataFrame) -> pd.DataFrame:
    if isinstance(df_in, pl.DataFrame):
        df_out = df_in.to_pandas()
    else:
        df_out = df_in.copy()
        # .copy() drops a user-set `name` attribute, which skim uses as the
        # heading of the Data Summary table, so carry it across.
        if "name" not in df_in.columns and hasattr(df_in, "name"):
            # stubs read .name as a column; here it is a plain attribute
            df_out.name = df_in.name  # ty: ignore[invalid-assignment]
    if df_out.columns.has_duplicates:
        df_out.columns = _deduplicate_column_names(df_out.columns)
    return df_out


def _deduplicate_column_names(names: pd.Index) -> list[Any]:
    """Rename duplicated column names by appending _1, _2, etc., and warn.

    Suffixes skip any name already in use, so the result is always unique.
    """
    taken = {str(name) for name in names}
    seen: set[Any] = set()
    new_names: list[Any] = []
    renamed: dict[Any, list[str]] = defaultdict(list)
    for name in names:
        if name not in seen:
            seen.add(name)
            new_names.append(name)
            continue
        suffix = 1
        while f"{name}_{suffix}" in taken:
            suffix += 1
        new_name = f"{name}_{suffix}"
        taken.add(new_name)
        new_names.append(new_name)
        renamed[name].append(new_name)
    details = "; ".join(f"{old!r} -> {', '.join(new)}" for old, new in renamed.items())
    warnings.warn(
        f"Duplicate column names were renamed for this summary: {details}. "
        "Your dataframe has not been changed.",
        UserWarning,
        stacklevel=4,
    )
    return new_names


@typechecked
def skim_get_data(
    df_in: pd.DataFrame | pl.DataFrame,
) -> JSON | str:
    """Skim a pandas or polars dataframe and return summary statistics as a dictionary, and without printing to the console.

    skim is an alternative to pandas.DataFrame.describe(), quickly providing
    an overview of a data frame via a table of summary statistics. It produces a different set of summary
    functions based on the types of columns in the dataframe. You may get
    better results from ensuring that you set the datatypes in your dataframe
    you want before running skim.

    Note that any unknown column types, or mixed column types, will not be
    processed.

    Args:
        df_in (pd.DataFrame | pl.DataFrame): Dataframe to get summary statistics on.

    Returns:
        JSON | str: Dictionary of summary statistics.
    """
    df_out = _convert_to_pandas(df_in)
    _, json_data = _skim_computation(df_out)
    return json_data


@typechecked
def skim_get_figure(
    df_in: pd.DataFrame | pl.DataFrame,
    save_path: os.PathLike | str,
    format: str = "svg",
) -> None:
    """Skim a pandas or polars dataframe, print the stats to the console, and save a version of the table as an SVG, HTML, or text file.

    skim is an alternative to pandas.DataFrame.describe(), quickly providing
    an overview of a data frame via a table of summary statistics. It produces a different set of summary
    functions based on the types of columns in the dataframe. You may get
    better results from ensuring that you set the datatypes in your dataframe
    you want before running skim.

    Note that any unknown column types, or mixed column types, will not be
    processed.

    Args:
        df_in (pd.DataFrame | pl.DataFrame): Dataframe to skim.
        save_path (os.PathLike | str): Path to save figure to (include extension).
        format (str, optional): svg, html, or text. Defaults to "svg".

    Raises:
        ValueError: If the format is not one of svg, html, or text.
    """
    df_out = _convert_to_pandas(df_in)
    grid, _ = _skim_computation(df_out)
    console = Console(record=True)
    console.print(Panel(grid, title="skimpy summary", subtitle="End"))
    if not isinstance(save_path, str):
        save_path_str = str(save_path)
    else:
        save_path_str = save_path
    match format.lower():
        case "svg":
            console.save_svg(save_path_str)
        case "html":
            console.save_html(save_path_str)
        case "text":
            console.save_text(save_path_str)
        case _:
            raise ValueError("Format must be: svg, html, or text")


@typechecked
def clean_columns(
    df: pd.DataFrame | pl.DataFrame,
    case: str = "snake",
    replace: dict[str, str] | None = None,
    remove_accents: bool = True,
) -> pd.DataFrame | pl.DataFrame:
    """Clean messy column names in a pandas dataframe.

    Args:
        df (pd.DataFrame | pl.DataFrame): Dataframe from which column names are to be cleaned.
        case (str, optional): The desired case style of the column name. Defaults to "snake".

                - 'snake' produces 'column_name';
                - 'kebab' produces 'column-name';
                - 'camel' produces 'columnName';
                - 'pascal' produces 'ColumnName';
                - 'const' produces 'COLUMN_NAME';
                - 'sentence' produces 'Column name';
                - 'title' produces 'Column Name';
                - 'lower' produces 'column name';
                - 'upper' produces 'COLUMN NAME';

        replace (dict[str, str] | None, optional): Values to replace in the column names. Defaults to None.

                - {'old_value': 'new_value'}

        remove_accents (bool, optional): If True, strip accents from the column names. Defaults to True.

    Raises:
        ValueError: If case is not valid.

    Returns:
        pd.DataFrame | pl.DataFrame: Dataframe with cleaned column names.

    Examples:
        Clean column names by converting the names to camel case style, removing accents,
        and correcting a mispelling.

        >>> df = pd.DataFrame(
                            {
                            'FirstNom': ['Philip', 'Turanga'],
                            'lastName': ['Fry', 'Leela'],
                            'Téléphone': ['555-234-5678', '(604) 111-2335']
                            })

        >>> clean_columns(df, case='camel', replace={'Nom': 'Name'})
        firstName lastName       telephone
        0    Philip      Fry    555-234-5678
        1   Turanga    Leela  (604) 111-2335
    """
    if case not in CASE_STYLES:
        raise ValueError(
            f"case {case} is invalid, options are: {', '.join(c for c in CASE_STYLES)}"
        )

    # Work on the list of names, then apply them in one go. Renaming column by
    # column would fail on Polars, which rejects the duplicate names that
    # cleaning can create before _rename_duplicates has numbered them.
    names = list(df.columns)
    if replace:
        names = [_replace_values(col, replace) for col in names]
    if remove_accents:
        names = [_remove_accents(col) for col in names]
    names = [_convert_case(col, case) for col in names]
    names = _rename_duplicates(names, case)

    if isinstance(df, pd.DataFrame):
        return df.set_axis(names, axis=1)
    df = df.clone()
    df.columns = names
    return df


@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name


@typechecked
def _split_strip_string(string: str) -> list[str]:
    """Split the string into separate words and strip punctuation."""
    string = re.sub(r"[!()*+\,\-./:;<=>?[\]^_{|}~]", " ", string)
    string = re.sub(r"[\'\"\`]", "", string)

    return re.sub(
        r"([A-Z][a-z]+)", r" \1", re.sub(r"([A-Z]+|[0-9]+|\W+)", r" \1", string)
    ).split()


@typechecked
def _split_string(string: str) -> list[str]:
    """Split the string into separate words."""
    string = re.sub(r"[\-_]", " ", string)

    return re.sub(r"([A-Z][a-z]+)", r" \1", re.sub(r"([A-Z]+)", r"\1", string)).split()


@typechecked
def _replace_values(name: Any, mapping: dict[str, str]) -> Any:
    """_summary_

    Args:
        name (Any): Column name.
        mapping (dict[str, str]): Maps old values in the column name to the new values.

    Returns:
        Any: Re-mapped column name.
    """
    if name in NULL_VALUES:
        return name

    name = str(name)
    for old_value, new_value in mapping.items():
        # If the old value or the new value is not alphanumeric, add underscores to the
        # beginning and end so the new value will be parsed correctly for _convert_case()
        new_val = (
            rf"{new_value}"
            if old_value.isalnum() and new_value.isalnum()
            else rf"_{new_value}_"
        )
        name = re.sub(rf"{old_value}", new_val, name, flags=re.IGNORECASE)

    return name


@typechecked
def _remove_accents(name: Any) -> Any:
    """Return the normal form for a Unicode string name using canonical decomposition."""
    if not isinstance(name, str):
        return name

    return normalize("NFD", name).encode("ascii", "ignore").decode("ascii")


@typechecked
def _rename_duplicates(names: pd.Index | list[str], case: str) -> Any:
    """Rename duplicated column names to append a number at the end."""
    if case in {"snake", "const"}:
        sep = "_"
    elif case in {"camel", "pascal"}:
        sep = ""
    elif case == "kebab":
        sep = "-"
    else:
        sep = " "

    names = list(names)
    counts: dict[str, int] = {}

    for i, col in enumerate(names):
        cur_count = counts.get(col, 0)
        if cur_count > 0:
            names[i] = f"{col}{sep}{cur_count}"
        counts[col] = cur_count + 1

    return names


@typechecked
def generate_test_data() -> pd.DataFrame:
    """Generate a pandas dataframe with several different datatypes.

    For testing skimpy, it's convenient to have a dataset with many different
    data types. This function creates that dataframe.

    Returns:
        pd.DataFrame: dataframe with columns spanning several data types.

    Examples:
        Generate test data to demonstrate how skimpy works.

        >>> df = generate_test_data()
    """
    seed = 34729
    rng = Generator(PCG64(seed))
    len_df = 1000
    df = pd.DataFrame()
    df["length"] = rng.beta(0.5, 0.5, size=len_df)
    df["width"] = rng.gamma(1, 2, size=len_df)
    df["depth"] = rng.poisson(10, size=len_df)
    df["rnd"] = rng.normal(size=len_df, scale=1, loc=0)
    nan_places = rng.choice(range(len_df), size=125).tolist()
    df.loc[nan_places, "rnd"] = np.nan
    df["class"] = rng.choice(["setosa", "virtginica"], size=len_df)
    df["class"] = df["class"].astype("category")
    second_cat_var_entries = ["UK", "Mexico", "USA", "India"]
    prob = [0.6, 0.2, 0.1, 0.1]
    df["location"] = rng.choice(second_cat_var_entries, len_df, p=prob)
    df["location"] = df["location"].astype("category")
    df.loc[3, "location"] = np.nan
    df["booly_col"] = rng.choice([True, False], size=len_df)
    df["booly_col"] = df["booly_col"].astype(bool)
    # string column
    string_options = [
        "How are you?",
        "What weather!",
        "Indeed, it was the most outrageously pompous cat I have ever seen.",
    ]
    df["text"] = rng.choice(string_options, len_df)
    df.loc[[3, 5, 8, 9, 14, 22], "text"] = None
    df["text"] = df["text"].astype("string")
    # add a datetime column
    df["datetime"] = pd.date_range("2018-01-01", periods=len_df, freq="ME")
    df["datetime_no_freq"] = rng.choice(
        (pd.to_datetime(pd.Series(["01/01/2022", "03/04/2023", "01/05/1992"]))), len_df
    )
    df["datetime.date"] = df["datetime"].dt.date
    df["datetime.date_no_freq"] = df["datetime_no_freq"].dt.date
    df.loc[[3, 12, 0], "datetime_no_freq"] = pd.NaT
    timedelta_array = rng.multinomial(40, [1 / 7] * 5, len_df).ravel()
    df["time diff"] = pd.Series([pd.Timedelta(int(x), "D") for x in timedelta_array])
    df.loc[[22, 1, 13, 65, 120], "time diff"] = pd.NaT
    return df
