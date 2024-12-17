"""Test cases for the __main__ module."""

import datetime
import os
import subprocess

import numpy as np
import pandas as pd
import polars as pl
import pytest
from click.testing import CliRunner
from pandas.testing import assert_frame_equal
from skimpy import (
    __main__,
    _bool_variable_summary_table,
    _convert_case,
    _infer_datatypes,
    _map_row_positions_to_text_style,
    _replace_values,
    _round_series,
    _simplify_datetimes_in_array,
    _string_variable_summary_table,
    clean_columns,
    generate_test_data,
    skim,
    skim_get_data,
    skim_get_figure,
)
from typeguard import typeguard_ignore


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
        "object",
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
            "header": [pd.Timedelta(365, "d"), pd.Timedelta(-19, "d")],
            "header_1": ["length_one", "length_two"],
        }
    )
    skim(df_check)
    assert type(df_check["header"].iloc[0]) == pd._libs.tslibs.timedeltas.Timedelta


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


def test_017_create_readme_doc() -> None:
    """Test that the readme.md can be created"""
    cmd_str = "poetry run jupyter nbconvert --to markdown --execute docs/index.ipynb"
    subprocess.run(cmd_str, shell=True)
    subprocess.run(["rm", "docs/index.md"])


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


def test_having_a_df_with_a_name():
    """Test where df has a specific name"""
    name_to_use = "test name passthrough"
    df = generate_test_data()
    df.name = name_to_use
    skim(df)


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
