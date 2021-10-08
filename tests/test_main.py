"""Test cases for the __main__ module."""
import datetime

import numpy as np
import pandas as pd
import pytest
from click.testing import CliRunner

from skimpy import __main__
from skimpy import generate_test_data
from skimpy import infer_datatypes
from skimpy import map_row_positions_to_text_style
from skimpy import simplify_datetimes_in_array
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
    df = infer_datatypes(df)
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
    row_dict = map_row_positions_to_text_style(datatype_justify, df)
    assert answers == row_dict


def test_007_simplify_datetimes_in_array() -> None:
    """Tests whether datetimes in an array are simplified."""
    df = pd.DataFrame()
    df["date"] = pd.date_range(start="2001-01-01", periods=3, freq="M")
    df["other"] = ["a", "b", "c"]
    rows = df.values
    rows = simplify_datetimes_in_array(rows)
    assert list(rows[:, 0]) == list(
        df["date"].apply(lambda x: str(x)).str.split(" ", expand=True).loc[:, 0].values
    )
