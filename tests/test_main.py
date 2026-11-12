"""Test cases for the __main__ module."""

import datetime
import decimal
import io
import os
import warnings

import numpy as np
import pandas as pd
import polars as pl
import pytest
from click.testing import CliRunner
from pandas.testing import assert_frame_equal
from rich.console import Console
from typeguard import typeguard_ignore

from skimpy import (
    __main__,
    _bool_variable_summary_table,
    _compute_column_widths,
    _convert_case,
    _infer_datatypes,
    _map_row_positions_to_text_style,
    _replace_values,
    _round_series,
    _simplify_datetimes_in_array,
    _skim_computation,
    _string_variable_summary_table,
    clean_columns,
    generate_test_data,
    skim,
    skim_get_data,
    skim_get_figure,
)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    with runner.isolated_filesystem():
        df = generate_test_data()
        df.to_csv("test_file.csv", index=False)
        result = runner.invoke(__main__.main, ["test_file.csv"])
        assert result.exit_code == 0


def test_000_basic_functionality() -> None:
    """Tests that a skim of the test data works."""
    df = generate_test_data()
    skim(df)


def test_003_not_enough_datetimes() -> None:
    """Tests logic branch with too few datetimes for freq inference."""
    df = generate_test_data()
    df = df.head(2)
    skim(df)


def test_004_when_df_is_named() -> None:
    """Tests what happens when df has a name."""
    df = generate_test_data()
    df.name = "Named dataframe"
    skim(df)


def test_005_inference_datatypes() -> None:
    """Tests the inference of datatypes."""
    data = (
        [datetime.datetime(2021, 1, 1), None, "as", 6],
        [datetime.datetime(2021, 1, 2), 5.2, "asd", 7],
        [None, 6.3, "adasda", 8],
    )
    df = pd.DataFrame(data, columns=["date", "float", "string", "integer"])
    df["cat"] = ["a", "b", "b"]
    df["cat"] = df["cat"].astype("category")
    df["date2"] = pd.date_range(start="2001-01-01", periods=3, freq="ME")
    df["booly"] = [True, True, False]
    # as example that isn't supported
    df["complex"] = np.array([[1 + 1j], [1 + 1j], [1 + 1j]])
    df["actual_date"] = df["date2"].dt.date
    df = _infer_datatypes(df)
    dtypes = df.dtypes.apply(lambda x: str(x)).str.split(r"(\d+)").str[0]
    assert list(dtypes) == [
        "datetime",
        "float",
        "string",
        "int",
        "category",
        "datetime",
        "bool",
        "complex",
        "date",
    ]


def test_006_test_row_map() -> None:
    """Tests the mapping of properties to positions in dataframes."""
    df = pd.DataFrame.from_dict(
        {"a": [0.43, 4.0], "b": ["string", "string"], "c": [594, 909]}
    )
    df["a"] = df["a"].astype("float")
    df["c"] = df["c"].astype("int")
    df["b"] = df["b"].astype("string")
    datatype_justify = {
        "number": "right",
        "category": "center",
        "datetime": "center",
        "string": "center",
        "bool": "left",
        "object": "left",
    }
    answers = {
        0: datatype_justify["number"],
        1: datatype_justify["string"],
        2: datatype_justify["number"],
    }
    row_dict = _map_row_positions_to_text_style(datatype_justify, df)
    assert answers == row_dict


@typeguard_ignore
def test_007_simplify_datetimes_in_array() -> None:
    """Tests whether datetimes in an array are simplified."""
    df = pd.DataFrame()
    df["date"] = pd.date_range(start="2001-01-01", periods=3, freq="ME")
    df = pd.concat(
        [
            df,
            pd.DataFrame.from_dict(
                {"date": pd.to_datetime("2001-04-01 17:43:21")}, orient="index"
            ).T,
        ],
        axis=0,
    )
    df = df.reset_index(drop=True)
    df["other"] = ["a", "b", "c", "d"]
    rows = df.values
    rows = _simplify_datetimes_in_array(rows)
    assert list(rows[:-1, 0]) == list(
        df["date"]
        .apply(lambda x: str(x))
        .str.split(" ", expand=True)
        .loc[:, 0]
        .values[:-1]
    )
    assert rows[-1, 0] == df["date"].iloc[-1]


def test_007_horrible_column_names() -> None:
    """Tests the cleaning of column names."""
    bad_columns = [
        "bs lncs;n edbn ",
        "Nín hǎo. Wǒ shì zhōng guó rén",
        "___This is a test___",
        "ÜBER Über German Umlaut",
    ]
    df = pd.DataFrame(columns=bad_columns, index=[0], data=[range(len(bad_columns))])
    df = clean_columns(df)
    assert list(df.columns) != bad_columns


@pytest.fixture(scope="module")  # type: ignore
def df_headers() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "ISBN": [9781455582341],
            "isbn": [1455582328],
            "bookTitle": ["How Google Works"],
            "__Author": ["Eric Schmidt, Jonathan Rosenberg"],
            "Publication (year)": [2014],
            "éditeur": ["Grand Central Publishing"],
            "Number_Of_Pages": [305],
            "★ Rating": [4.06],
        }
    )
    return df


@pytest.fixture(scope="module")  # type: ignore
def df_null_headers() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "": [9781455582341],
            np.nan: ["How Google Works"],
            None: ["Eric Schmidt, Jonathan Rosenberg"],
            "N/A": [2014],
        }
    )
    return df


@typeguard_ignore
def test_008_clean_default(df_headers: pd.DataFrame) -> None:
    df_clean = clean_columns(df_headers)
    df_check = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn_1": [1455582328],
            "book_title": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publication_year": [2014],
            "editeur": ["Grand Central Publishing"],
            "number_of_pages": [305],
            "rating": [4.06],
        }
    )
    assert df_check.equals(df_clean)


@typeguard_ignore
def test_009_clean_case_style(df_headers: pd.DataFrame) -> None:
    df_clean_kebab = clean_columns(df_headers, case="kebab")
    df_clean_camel = clean_columns(df_headers, case="camel")
    df_clean_pascal = clean_columns(df_headers, case="pascal")
    df_clean_const = clean_columns(df_headers, case="const")
    df_clean_sentence = clean_columns(df_headers, case="sentence")
    df_clean_title = clean_columns(df_headers, case="title")
    df_clean_lower = clean_columns(df_headers, case="lower")
    df_clean_upper = clean_columns(df_headers, case="upper")
    df_check_kebab = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn-1": [1455582328],
            "book-title": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publication-year": [2014],
            "editeur": ["Grand Central Publishing"],
            "number-of-pages": [305],
            "rating": [4.06],
        }
    )
    df_check_camel = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn1": [1455582328],
            "bookTitle": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publicationYear": [2014],
            "editeur": ["Grand Central Publishing"],
            "numberOfPages": [305],
            "rating": [4.06],
        }
    )
    df_check_pascal = pd.DataFrame(
        {
            "Isbn": [9781455582341],
            "Isbn1": [1455582328],
            "BookTitle": ["How Google Works"],
            "Author": ["Eric Schmidt, Jonathan Rosenberg"],
            "PublicationYear": [2014],
            "Editeur": ["Grand Central Publishing"],
            "NumberOfPages": [305],
            "Rating": [4.06],
        }
    )
    df_check_const = pd.DataFrame(
        {
            "ISBN": [9781455582341],
            "ISBN_1": [1455582328],
            "BOOK_TITLE": ["How Google Works"],
            "AUTHOR": ["Eric Schmidt, Jonathan Rosenberg"],
            "PUBLICATION_YEAR": [2014],
            "EDITEUR": ["Grand Central Publishing"],
            "NUMBER_OF_PAGES": [305],
            "RATING": [4.06],
        }
    )
    df_check_sentence = pd.DataFrame(
        {
            "Isbn": [9781455582341],
            "Isbn 1": [1455582328],
            "Book title": ["How Google Works"],
            "Author": ["Eric Schmidt, Jonathan Rosenberg"],
            "Publication (year)": [2014],
            "Editeur": ["Grand Central Publishing"],
            "Number of pages": [305],
            "Rating": [4.06],
        }
    )
    df_check_title = pd.DataFrame(
        {
            "Isbn": [9781455582341],
            "Isbn 1": [1455582328],
            "Book Title": ["How Google Works"],
            "Author": ["Eric Schmidt, Jonathan Rosenberg"],
            "Publication (year)": [2014],
            "Editeur": ["Grand Central Publishing"],
            "Number Of Pages": [305],
            "Rating": [4.06],
        }
    )
    df_check_lower = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn 1": [1455582328],
            "book title": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publication (year)": [2014],
            "editeur": ["Grand Central Publishing"],
            "number of pages": [305],
            "rating": [4.06],
        }
    )
    df_check_upper = pd.DataFrame(
        {
            "ISBN": [9781455582341],
            "ISBN 1": [1455582328],
            "BOOK TITLE": ["How Google Works"],
            "AUTHOR": ["Eric Schmidt, Jonathan Rosenberg"],
            "PUBLICATION (YEAR)": [2014],
            "EDITEUR": ["Grand Central Publishing"],
            "NUMBER OF PAGES": [305],
            "RATING": [4.06],
        }
    )
    assert df_check_kebab.equals(df_clean_kebab)
    assert df_check_camel.equals(df_clean_camel)
    assert df_check_pascal.equals(df_clean_pascal)
    assert df_check_const.equals(df_clean_const)
    assert df_check_sentence.equals(df_clean_sentence)
    assert df_check_title.equals(df_clean_title)
    assert df_check_lower.equals(df_clean_lower)
    assert df_check_upper.equals(df_clean_upper)


@typeguard_ignore
def test_010_clean_replace(df_headers: pd.DataFrame) -> None:
    df_clean = clean_columns(df_headers, replace={"éditeur": "publisher", "★": "star"})
    df_check = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn_1": [1455582328],
            "book_title": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publication_year": [2014],
            "publisher": ["Grand Central Publishing"],
            "number_of_pages": [305],
            "star_rating": [4.06],
        }
    )
    assert df_check.equals(df_clean)


@typeguard_ignore
def test_011_clean_keep_accents(df_headers: pd.DataFrame) -> None:
    df_clean = clean_columns(df_headers, remove_accents=False)
    df_check = pd.DataFrame(
        {
            "isbn": [9781455582341],
            "isbn_1": [1455582328],
            "book_title": ["How Google Works"],
            "author": ["Eric Schmidt, Jonathan Rosenberg"],
            "publication_year": [2014],
            "éditeur": ["Grand Central Publishing"],
            "number_of_pages": [305],
            "★_rating": [4.06],
        }
    )
    assert df_check.equals(df_clean)


@typeguard_ignore
def test_012_clean_null_headers(df_null_headers: pd.DataFrame) -> None:
    df_clean = clean_columns(df_null_headers)
    df_check = pd.DataFrame(
        {
            "header": [9781455582341],
            "header_1": ["How Google Works"],
            "header_2": ["Eric Schmidt, Jonathan Rosenberg"],
            "n_a": [2014],
        }
    )
    assert df_check.equals(df_clean)


def test_013_convert_case_upper() -> None:
    in_string = "bHlah lower case"
    assert _convert_case(in_string, case="upper") == "B HLAH LOWER CASE"


def test_014_user_contrib_two_object_cols() -> None:
    DATA_URL = "https://raw.githubusercontent.com/DataBooth/data-public/main/beach-safe/nsw_beach_rss_list.csv"
    df = pd.read_csv(DATA_URL)
    skim(df)


def test_015_ensure_no_data_changed() -> None:
    """Found a bug where time deltas were changed after skimpy being used.
    Using a copying strategy to avoid; test checks it actually fixed the bug.
    """
    df_check = pd.DataFrame(
        {
            "header": [pd.Timedelta(365, "D"), pd.Timedelta(-19, "D")],
            "header_1": ["length_one", "length_two"],
        }
    )
    skim(df_check)
    assert isinstance(df_check["header"].iloc[0], pd.Timedelta)


def test_016_long_col_names() -> None:
    """User raised issue with behaviour when column names are long."""
    df = generate_test_data()
    df = df.rename(
        columns={
            "length": "this_is_the_length_col_long_name",
            "location": "this_is_a_longwinded_way_of_saying_location_column",
        }
    )
    skim(df)


def test_18_empty_dataframe_infer_type():
    """Test empty DataFrame input."""
    empty_df = pd.DataFrame()
    result = _infer_datatypes(empty_df)
    assert_frame_equal(result, empty_df)


def test_19_infer_various_data_types():
    """Test DataFrame with various data types."""
    data = {
        "string_col": ["apple", "banana", "orange"],
        "int_col": [1, 2, 3],
        "float_col": [1.1, 2.2, 3.3],
        "timedelta_col": pd.to_timedelta([1, 2, 3], unit="D"),
        "datetime_col": pd.to_datetime(["2023-07-22", "2023-07-23", "2023-07-24"]),
        "categorical_col": pd.Categorical(["cat", "dog", "bird"]),
        "bool_col": [True, False, True],
    }
    df = pd.DataFrame(data)
    result = _infer_datatypes(df)
    # NB: Windows uses int32 sometimes so need to only compare trunk datatype
    resulting_dtypes = list(
        result.dtypes.astype("string").str.split("[1-9][0-9]", regex=True).str[0]
    )
    expected_data_types = [
        "string",
        "int",
        "float",
        "timedelta",
        "datetime",
        "category",
        "bool",
    ]
    assert resulting_dtypes == expected_data_types


def test_20_unsupported_data_types():
    """Test currently unsupported data types."""
    data = {
        "complex_col": [1 + 2j, 3 + 4j, 5 + 6j],
    }
    df = pd.DataFrame(data)
    result = _infer_datatypes(df)
    expected_data_types = ["complex128"]
    assert list(result.dtypes.astype("string").values) == expected_data_types


def test_21_dataframe_with_null_values():
    """Test DataFrame with null (None) values."""
    data = {
        "col1": [1, None, 3],
        "col2": [None, 2, None],
        "col3": [1.1, 2.2, None],
    }
    df = pd.DataFrame(data)
    result = _infer_datatypes(df)
    expected_data_types = ["float64"] * 3
    assert list(result.dtypes.astype("string").values) == expected_data_types


def test_22_string_summary():
    """test summarising string columns of dataframes."""
    string_list = [
        "How are you?",
        "What weather!",
        "Indeed, it was the most outrageously pompous cat I have ever seen.",
        "",
        "blah",
    ]
    df = pd.DataFrame(string_list, columns=["text"], dtype="string")
    df.loc[[3], "text"] = None
    result_df = _string_variable_summary_table(df)
    expected_values = [
        1,
        20.0,
        "blah",
        "Indeed, it was the most outrageously pompous cat I have ever seen.",
        "How are you?",
        "blah",
        23.8,
        3.6,
        18,
    ]
    for i, col in enumerate(result_df.columns):
        assert result_df.iloc[0, i] == expected_values[i]


def test_22a_string_summary_respects_non_default_index():
    """shortest/longest must refer to the correct row even when the
    dataframe's index isn't the default 0..n-1 range, eg after filtering."""
    df = pd.DataFrame({"text": ["zzzzzzzzzz", "a", "mmm"]}, dtype="string")
    df.index = [2, 0, 1]
    result_df = _string_variable_summary_table(df)
    assert result_df.loc["text", "shortest"] == "a"
    assert result_df.loc["text", "longest"] == "zzzzzzzzzz"


def test_23_bool_summary():
    """test summarising bool columns of dataframes."""
    bool_list = [
        True,
        False,
        None,  # interpreted as False
        True,
    ]
    df = pd.DataFrame(bool_list, columns=["bool"], dtype="bool")
    result_df = _bool_variable_summary_table(df)
    expected_values = [2, 0.5, "▇    ▇"]
    if os.name == "posix":
        expected_values = [2, 0.5, "█    █"]
    for i, col in enumerate(result_df.columns):
        assert result_df.iloc[0, i] == expected_values[i]


def test_24_round_series():
    """Rounding."""
    ints_to_round = [10001, 9999, 101, 99, 1, 0, -9, -251]
    doubles_to_round = [10001.543, 0.99, -0.643, 20.1]
    assert list(_round_series(pd.Series(ints_to_round)).values) == list(
        np.array([1.0e04, 1.0e04, 1.0e02, 9.9e01, 1.0e00, 0.0e00, -9.0e00, -2.5e02])
    )
    assert list(_round_series(pd.Series(doubles_to_round)).values) == list(
        np.array([10000.0, 0.99, -0.64, 20.0])
    )


def test_25_column_with_mixed_type():
    """Columns of residual object type, or mixed columns, alongside useful ones."""
    data_list = [
        "How are you?",
        23,
        True,
        304.92048,
    ]
    df = pd.DataFrame(data_list, columns=["object_col"], dtype="object")
    # useful to throw in a date here as it's also of type object
    df["date"] = pd.to_datetime("2003-01-01 00:00:00")
    df["date"] = df["date"].dt.date
    df["other_real_data"] = 55.008
    skim(df)


def test_26_only_unsupported_columns():
    """test that an error is raised when only unsupported columns are passed."""
    with pytest.raises(ValueError):
        data_list = [
            "How are you?",
            23,
            True,
            304.92048,
        ]
        df = pd.DataFrame(data_list, columns=["object_col"], dtype="object")
        skim(df)


def test_27_missing_case_entered():
    """Test for value error when case is misspecified."""
    with pytest.raises(ValueError):
        df = pd.DataFrame(
            {
                "FirstNom": ["Philip", "Turanga"],
                "lastName": ["Fry", "Leela"],
                "Téléphone": ["555-234-5678", "(604) 111-2335"],
            }
        )
        clean_columns(df, case="FAKECASE", replace={"Nom": "Name"})


def test_28_special_name_values():
    """There are special null column names that complicate replace name ops."""
    ans_one = _replace_values(np.nan, {"Philip": "new_name"})
    ans_two = _replace_values(None, {"Fry": "new_name"})
    ans_three = _replace_values("", {"555-234-5678": "new_name"})
    ans_list = [ans_one, ans_two, ans_three]
    assert ans_list == [np.nan, None, ""]


def test_29_json_return_data():
    """Test the return data function. Nerfed for the benefit of Windows."""
    data = {
        "string_col": ["apple", "banana", "orange"],
        "int_col": [1, 2, 3],
        "float_col": [1.1, 2.2, 3.3],
        "timedelta_col": pd.to_timedelta([1, 2, 3], unit="D"),
        "datetime_col": pd.to_datetime(["2023-07-22", "2023-07-23", "2023-07-24"]),
        "categorical_col": pd.Categorical(["cat", "dog", "bird"]),
        "bool_col": [True, False, True],
    }
    df = pd.DataFrame(data)
    ret_json = skim_get_data(df)
    # only compare keys because of Windows' integer preferences (int32 over int64)
    ret_json_keys = list(ret_json.keys())
    expected_output = [
        "Data Summary",
        "Data Types",
        "Categories",
        "number",
        "category",
        "bool",
        "datetime",
        "timedelta64[ns]",
        "string",
    ]
    assert ret_json_keys == expected_output


def test_date_section_has_readable_name() -> None:
    """Python date columns get a "date" section, not "<class 'datetime.date'>"."""
    df = pd.DataFrame({"day": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)]})
    ret_json = skim_get_data(df)
    assert "date" in ret_json
    assert not any("datetime.date" in key for key in ret_json)
    assert ret_json["date"]["first"]["day"] == datetime.date(2023, 1, 1)


def test_timedelta_summary_reports_median() -> None:
    """The timedelta median must not be reported as its minimum."""
    frame = pd.DataFrame({"elapsed": pd.to_timedelta([1, 2, 100], unit="h")})

    result = skim_get_data(frame)

    assert result["timedelta64[ns]"]["median"]["elapsed"] == pd.Timedelta(hours=2)


def test_30_running_with_polars():
    """Tests the polars skim functionality."""
    df1 = pl.DataFrame(
        {
            "foo": [1, 2, 3],
            "bar": [6, 7, 8],
            "ham": ["a", "b", "c"],
        }
    )
    skim(df1)


def test_running_with_polars_return_data():
    """Tests the polars skim functionality."""
    df1 = pl.DataFrame(
        {
            "foo": [1, 2, 3],
            "bar": [6, 7, 8],
            "ham": ["a", "b", "c"],
        }
    )
    polars_tbl_out = skim_get_data(df1)
    pandas_tbl_out = skim_get_data(df1.to_pandas())
    assert pandas_tbl_out == polars_tbl_out


def test_exporting_to_svg(tmp_path):
    """Export results to a file."""
    df = generate_test_data()
    skim_get_figure(df, save_path=tmp_path / "blah.svg")


def test_exporting_to_html(tmp_path):
    """Export results to a file."""
    df = generate_test_data()
    skim_get_figure(df, save_path=tmp_path / "blah.html", format="html")


def test_exporting_to_text(tmp_path):
    """Export results to a file."""
    df = generate_test_data()
    skim_get_figure(df, save_path=tmp_path / "blah.txt", format="text")


def test_cleaning_polars_columns():
    """Tests the polars rename columns functionality."""
    bad_columns = [
        "bs lncs;n edbn ",
        "Nín hǎo. Wǒ shì zhōng guó rén",
        "___This is a test___",
        "ÜBER Über German Umlaut",
    ]
    df = pl.DataFrame(
        {
            bad_columns[0]: [1, 2, 3, 4],
            bad_columns[1]: [1, 2, 3, 4],
            bad_columns[2]: [1, 2, 3, 4],
            bad_columns[3]: [1, 2, 3, 4],
        }
    )
    df = clean_columns(df)
    assert list(df.columns) != bad_columns


def test_cleaning_polars_columns_that_become_duplicates():
    """Names that clean to the same value are numbered, not an error."""
    df = pl.DataFrame({"Total Sales": [1], "total-sales": [2], "TOTAL SALES": [3]})
    assert clean_columns(df).columns == [
        "total_sales",
        "total_sales_1",
        "total_sales_2",
    ]
    assert clean_columns(df, case="camel").columns == [
        "totalSales",
        "totalSales1",
        "totalSales2",
    ]
    # the input is left unchanged
    assert df.columns == ["Total Sales", "total-sales", "TOTAL SALES"]


def test_having_a_df_with_a_name(tmp_path):
    """A df's name attribute is used as the Data Summary heading."""
    name_to_use = "test name passthrough"
    df = generate_test_data()
    df.name = name_to_use
    skim(df)
    out = tmp_path / "named.txt"
    skim_get_figure(df, out, format="text")
    assert name_to_use in out.read_text(encoding="utf-8")


def test_handling_of_pandas_multiindex():
    """Ensures errors appropriately in place to catch pandas multi-index."""
    arrays = [
        ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
    df = pd.DataFrame(pd.Series(np.random.randn(8), index=index))
    df = df.unstack()
    with pytest.raises(NotImplementedError):
        skim(df)


# New tests for parquet and sqlite functionality


def test_main_parquet_succeeds(runner: CliRunner) -> None:
    """Test that skimpy successfully reads a parquet file."""
    with runner.isolated_filesystem():
        # Create a simple parquet file without NA values to avoid type inference issues
        df = pd.DataFrame(
            {
                "name": ["Alice", "Bob", "Charlie"],
                "age": [25, 30, 35],
                "salary": [50000.0, 60000.0, 75000.0],
            }
        )
        df.to_parquet("test_file.parquet")

        result = runner.invoke(__main__.main, ["test_file.parquet"])
        assert result.exit_code == 0


def test_main_sqlite_succeeds(runner: CliRunner) -> None:
    """Test that skimpy successfully reads a SQLite database with --table flag."""
    import duckdb

    with runner.isolated_filesystem():
        # Create a simple SQLite database using duckdb
        df = pd.DataFrame(  # noqa: F841 (referenced by DuckDB SQL)
            {
                "name": ["Alice", "Bob", "Charlie"],
                "age": [25, 30, 35],
                "salary": [50000.0, 60000.0, 75000.0],
            }
        )
        conn = duckdb.connect("test_db.sqlite")
        conn.execute("CREATE TABLE employees AS SELECT * FROM df")
        conn.close()

        result = runner.invoke(__main__.main, ["test_db.sqlite", "-t", "employees"])
        assert result.exit_code == 0


def test_main_sqlite_without_table_shows_tables(runner: CliRunner) -> None:
    """Test that running skimpy on SQLite without -t shows available tables."""
    import duckdb

    with runner.isolated_filesystem():
        # Create a simple SQLite database using duckdb
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})  # noqa: F841
        conn = duckdb.connect("test_db.sqlite")
        conn.execute("CREATE TABLE employees AS SELECT * FROM df")
        conn.close()

        result = runner.invoke(__main__.main, ["test_db.sqlite"])
        assert result.exit_code != 0  # Expected to fail without --table
        assert (
            "Available tables" in str(result.exception)
            or "Available tables" in result.output
        )
        assert "employees" in str(result.exception) or "employees" in result.output


def test_main_sqlite_invalid_table(runner: CliRunner) -> None:
    """Test that skimpy errors when specifying a non-existent table."""
    import duckdb

    with runner.isolated_filesystem():
        # Create a simple SQLite database using duckdb
        df = pd.DataFrame({"name": ["Alice"], "age": [25]})  # noqa: F841
        conn = duckdb.connect("test_db.sqlite")
        conn.execute("CREATE TABLE employees AS SELECT * FROM df")
        conn.close()

        result = runner.invoke(__main__.main, ["test_db.sqlite", "-t", "nonexistent"])
        assert result.exit_code != 0
        assert (
            "not found" in str(result.exception).lower()
            or "not found" in result.output.lower()
        )
        assert "employees" in str(result.exception) or "employees" in result.output


def test_compute_column_widths() -> None:
    """Tests that _compute_column_widths returns sensible per-column widths."""
    df = pd.DataFrame(
        {
            "short": ["a", "b"],
            "medium_column_name": ["hello", "world"],
            "x": ["a very long cell value that exceeds the max", "short"],
        }
    )
    widths = _compute_column_widths(df)
    assert len(widths) == 3
    # "short" header is 5 chars, content is 1 char -> clamped to MIN_COL_WIDTH (6)
    assert widths[0] == 6
    # "medium_column_name" header is 18 chars, content is 5 -> 18
    assert widths[1] == 18
    # "x" header is 1 char, content is 44 chars -> clamped to MAX_COL_WIDTH (40)
    assert widths[2] == 40


def test_compute_column_widths_empty_dataframe() -> None:
    """Tests _compute_column_widths with an empty dataframe."""
    df = pd.DataFrame({"col_a": pd.Series(dtype="str"), "b": pd.Series(dtype="str")})
    widths = _compute_column_widths(df)
    assert len(widths) == 2
    # "col_a" is 5 chars -> 6 (min), "b" is 1 char -> 6 (min)
    assert widths[0] == 6
    assert widths[1] == 6


def test_duplicate_column_names_same_type():
    """Duplicate numeric column names are renamed with a warning, not an error."""
    df = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "a"])
    with pytest.warns(UserWarning, match="Duplicate column names"):
        skim(df)
    with pytest.warns(UserWarning, match="Duplicate column names"):
        data = skim_get_data(df)
    assert set(data["number"]["mean"]) == {"a", "a_1"}
    # The user's dataframe is left untouched
    assert list(df.columns) == ["a", "a"]


def test_duplicate_column_names_mixed_types():
    """Duplicate names on columns of different types are each summarised."""
    df = pd.DataFrame({"x": [1.0, 2.0], "y": ["p", "q"]})
    df["y"] = df["y"].astype("string")
    df.columns = ["a", "a"]
    with pytest.warns(UserWarning, match="Duplicate column names"):
        data = skim_get_data(df)
    assert "a" in data["number"]["mean"]
    assert "a_1" in data["string"]["words per row"]


def test_duplicate_column_names_avoid_existing_names():
    """Renamed columns never clash with names already in the dataframe."""
    df = pd.DataFrame([[1, 2, 3, 4]], columns=["a", "a", "a_1", "a"])
    with pytest.warns(UserWarning, match="'a' -> a_2, a_3"):
        data = skim_get_data(df)
    assert set(data["number"]["mean"]) == {"a", "a_1", "a_2", "a_3"}


def _sections_containing(ret_json: dict, col: str) -> list[str]:
    """Names of the summary sections in which a column appears."""
    skip = {"Data Summary", "Data Types", "Categories"}
    return [
        section
        for section, stats in ret_json.items()
        if section not in skip and any(col in vals for vals in stats.values())
    ]


def test_object_dates_get_date_dtype() -> None:
    """Columns of Python dates are given a real (pyarrow) date dtype."""
    df = pd.DataFrame({"day": [datetime.date(2023, 1, 1), None]})
    out = _infer_datatypes(df)
    assert str(out["day"].dtype) == "date32[day][pyarrow]"


def test_pyarrow_date_column_is_summarised() -> None:
    """A date32[pyarrow] column (with enough rows to infer a frequency) works."""
    days = pd.date_range("2023-01-01", periods=6, freq="D").date
    df = pd.DataFrame({"day": pd.Series(days).astype("date32[pyarrow]")})
    ret_json = skim_get_data(df)
    assert ret_json["date"]["first"]["day"] == datetime.date(2023, 1, 1)
    assert ret_json["date"]["last"]["day"] == datetime.date(2023, 1, 6)
    assert ret_json["date"]["frequency"]["day"] == "D"


def test_date_and_datetime_columns_route_to_one_section_each() -> None:
    """Every column appears in exactly one summary section."""
    stamps = pd.date_range("2023-01-31", periods=5, freq="ME")
    df = pd.DataFrame(
        {
            "stamp": stamps,
            "obj_date": stamps.date,
            "arrow_date": pd.Series(stamps.date).astype("date32[pyarrow]"),
            "text": pd.Series(list("abcde"), dtype="string"),
            "num": [1.0, 2.0, 3.0, 4.0, 5.0],
            "flag": [True, False, True, False, True],
            "gap": pd.to_timedelta([1, 2, 3, 4, 5], unit="D"),
        }
    )
    ret_json = skim_get_data(df)
    expected = {
        "stamp": "datetime",
        "obj_date": "date",
        "arrow_date": "date",
        "text": "string",
        "num": "number",
        "flag": "bool",
        "gap": "timedelta64[ns]",
    }
    for col, section in expected.items():
        assert _sections_containing(ret_json, col) == [section], col
    assert ret_json["datetime"]["frequency"]["stamp"] == "ME"
    assert ret_json["date"]["frequency"]["obj_date"] == "ME"


def test_frequency_inference_does_not_warn() -> None:
    """Frequency inference avoids pandas' deprecated string-returning path."""
    stamps = pd.date_range("2023-01-31", periods=5, freq="ME")
    df = pd.DataFrame({"stamp": stamps, "day": stamps.date})
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        warnings.simplefilter("error", FutureWarning)
        skim_get_data(df)


_N_ROWS = 5
_OTHER_INFERRED_TYPE_CASES = {
    # name: (column, expected section)
    "bytes": (pd.Series([b"a", b"b", b"c", None, b"e"], dtype=object), "object"),
    "time": (
        pd.Series([datetime.time(i) for i in range(_N_ROWS)], dtype=object),
        "object",
    ),
    "decimal": (
        pd.Series([decimal.Decimal(i) / 3 for i in range(_N_ROWS)], dtype=object),
        "number",
    ),
    "py_datetime": (
        pd.Series(
            [datetime.datetime(2020, 1, i + 1) for i in range(_N_ROWS)], dtype=object
        ),
        "datetime",
    ),
    "py_timedelta": (
        pd.Series([datetime.timedelta(days=i) for i in range(_N_ROWS)], dtype=object),
        "timedelta64[ns]",
    ),
    "period": (
        pd.Series(pd.period_range("2020-01", periods=_N_ROWS, freq="M")),
        "object",
    ),
    "interval": (pd.Series(pd.interval_range(0, _N_ROWS)), "object"),
}


@pytest.mark.parametrize("preceded_by_float", [False, True])
@pytest.mark.parametrize("case", list(_OTHER_INFERRED_TYPE_CASES))
def test_less_common_inferred_types_are_routed(
    case: str, preceded_by_float: bool
) -> None:
    """Each inferred type gets its own treatment, never another column's cast.

    Previously, types without a branch in _infer_datatypes either raised
    UnboundLocalError or were cast to the previous column's dtype.
    """
    column, expected_section = _OTHER_INFERRED_TYPE_CASES[case]
    df = pd.DataFrame({"x": column})
    if preceded_by_float:
        df.insert(0, "f", [1.5] * _N_ROWS)
    ret_json = skim_get_data(df)
    assert _sections_containing(ret_json, "x") == [expected_section]


def test_unsupported_types_are_left_unchanged() -> None:
    """Types with no better dtype to cast to keep their original dtype."""
    df = pd.DataFrame(
        {
            name: _OTHER_INFERRED_TYPE_CASES[name][0]
            for name in ["bytes", "time", "period", "interval"]
        }
    )
    out = _infer_datatypes(df.copy())
    assert out.dtypes.equals(df.dtypes)


def test_tz_aware_python_datetimes_become_naive() -> None:
    """Python datetimes with timezones (even mixed ones) keep their wall time."""
    tz_plus2 = datetime.timezone(datetime.timedelta(hours=2))
    tz_minus5 = datetime.timezone(datetime.timedelta(hours=-5))
    values = [
        datetime.datetime(2020, 1, 1, 9, tzinfo=tz_plus2),
        datetime.datetime(2020, 1, 2, 9, tzinfo=tz_minus5),
        None,
    ]
    out = _infer_datatypes(pd.DataFrame({"x": pd.Series(values, dtype=object)}))
    assert pd.api.types.is_datetime64_dtype(out["x"].dtype)  # tz-naive
    assert list(out["x"].iloc[:2]) == [
        pd.Timestamp("2020-01-01 09:00"),
        pd.Timestamp("2020-01-02 09:00"),
    ]
    assert out["x"].isna().iloc[2]


@pytest.mark.parametrize("unit", ["s", "ms", "us"])
def test_datetime64_units_are_preserved(unit: str) -> None:
    """Non-nanosecond datetimes keep their unit, including when timezone-aware."""
    values = np.array(["2020-01-01", "2021-01-01"], dtype=f"datetime64[{unit}]")
    df = pd.DataFrame({"naive": values})
    df["aware"] = df["naive"].dt.tz_localize("UTC")
    out = _infer_datatypes(df)
    assert str(out["naive"].dtype) == f"datetime64[{unit}]"
    assert str(out["aware"].dtype) == f"datetime64[{unit}]"


def test_out_of_nanosecond_range_datetimes_are_summarised() -> None:
    """Datetimes outside c. 1677-2262 (where nanoseconds overflow) work."""
    far = ["1500-01-01", "3000-06-01", "NaT", "2020-01-01"]
    df = pd.DataFrame(
        {
            "datetime64": np.array(far, dtype="datetime64[s]"),
            "py_datetime": pd.Series(
                [
                    datetime.datetime(1500, 1, 1),
                    datetime.datetime(3000, 6, 1),
                    None,
                    datetime.datetime(2020, 1, 1),
                ],
                dtype=object,
            ),
        }
    )
    ret_json = skim_get_data(df)
    for col in df.columns:
        assert ret_json["datetime"]["first"][col] == pd.Timestamp("1500-01-01")
        assert ret_json["datetime"]["last"][col] == pd.Timestamp("3000-06-01")
        assert ret_json["datetime"]["NA"][col] == 1


def test_out_of_nanosecond_range_timedeltas_are_summarised() -> None:
    """Timedeltas beyond c. 292 years (where nanoseconds overflow) work."""
    days = [200 * 365, 400 * 365, 1, 2]
    df = pd.DataFrame(
        {
            "timedelta64": np.array(days, dtype="timedelta64[D]").astype(
                "timedelta64[s]"
            ),
            "py_timedelta": pd.Series(
                [datetime.timedelta(days=d) for d in days], dtype=object
            ),
        }
    )
    out = _infer_datatypes(df.copy())
    assert str(out["timedelta64"].dtype) == "timedelta64[s]"
    ret_json = skim_get_data(df)
    for col in df.columns:
        assert ret_json["timedelta64[ns]"]["max"][col] == np.timedelta64(400 * 365, "D")


def _rendered_text(df: pd.DataFrame) -> str:
    """The skim summary as plain text, as a user would see it in the console."""
    grid, _ = _skim_computation(df)
    console = Console(record=True, width=250, file=io.StringIO())
    console.print(grid)
    return console.export_text()


def test_square_brackets_are_not_treated_as_markup() -> None:
    """dtype units like [s] and column names in brackets are shown verbatim."""
    days = pd.date_range("2024-01-01", periods=4, freq="D")
    df = pd.DataFrame(
        {
            "[b]bold?": days.astype("datetime64[s]"),
            "gap": pd.to_timedelta([1, 2, 3, 4], unit="D"),
            "[s]": pd.Categorical(list("abab")),
        }
    )
    df.name = "[red]frame"
    text = _rendered_text(df)
    for expected in [
        "datetime64[s]",  # Data Types table
        "timedelta64[ns]",  # section title
        "[b]bold?",  # column name in a section
        "[s]",  # column name in the Categories table
        "[red]frame",  # dataframe name
    ]:
        assert expected in text, expected


def test_na_percent_is_rounded() -> None:
    """NA % is rounded to 2 decimal places in every section."""
    df = pd.DataFrame(
        {
            "num": [1.0, None, 3.0, 4.0, 5.0, 6.0],
            "when": pd.to_datetime(["2024-01-01"] * 5 + [None]),
            "day": [datetime.date(2024, 1, 1)] * 5 + [None],
        }
    )
    ret_json = skim_get_data(df)
    assert ret_json["number"]["NA %"]["num"] == 16.67
    assert ret_json["datetime"]["NA %"]["when"] == 16.67
    assert ret_json["date"]["NA %"]["day"] == 16.67


def test_no_inferred_frequency_is_na() -> None:
    """When no frequency can be inferred, it is reported as "NA"."""
    irregular = pd.to_datetime(["2024-01-01", "2024-01-02", "2024-03-09", "2025-07-01"])
    df = pd.DataFrame({"when": irregular, "day": irregular.date})
    ret_json = skim_get_data(df)
    assert ret_json["datetime"]["frequency"]["when"] == "NA"
    assert ret_json["date"]["frequency"]["day"] == "NA"
