"""Test cases for the __main__ module."""
import datetime

import numpy as np
import pandas as pd
import pytest
from click.testing import CliRunner

from skimpy import __main__
from skimpy import _convert_case
from skimpy import _infer_datatypes
from skimpy import _map_row_positions_to_text_style
from skimpy import _simplify_datetimes_in_array
from skimpy import clean_columns
from skimpy import generate_test_data
from skimpy import skim


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


def test_001_colour_kwargs() -> None:
    """Tests that colour keyword arguments work."""
    df = generate_test_data()
    skim(df, datetime="chartreuse1")


def test_002_header_style() -> None:
    """Tests that the header style optional argument works."""
    df = generate_test_data()
    skim(df, header_style="italic green")


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
    df["date2"] = pd.date_range(start="2001-01-01", periods=3, freq="M")
    df["booly"] = [True, True, False]
    # as example that isn't supported
    df["complex"] = np.array([[1 + 1j], [1 + 1j], [1 + 1j]])
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


def test_007_simplify_datetimes_in_array() -> None:
    """Tests whether datetimes in an array are simplified."""
    df = pd.DataFrame()
    df["date"] = pd.date_range(start="2001-01-01", periods=3, freq="M")
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
