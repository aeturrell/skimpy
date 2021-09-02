"""Test cases for the __main__ module."""
import pandas as pd
import pytest
from click.testing import CliRunner

from skimpy import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_000_basic_functionality():
    """[summary]."""
    df = pd.DataFrame(
        [
            [5.1, 3.5, 1.4, 0.2, "setosa"],
            [4.9, 3, 1.4, 0.2, "setosa"],
            [4.7, 3.2, 1.3, 0.2, "setosa"],
            [4.6, 3.1, 1.5, 0.2, "setosa"],
            [5, 3.6, 1.4, 0.2, "setosa"],
            [5.4, 3.9, 1.7, 0.4, "setosa"],
            [4.6, 3.4, 1.4, 0.3, "setosa"],
            [5, 3.4, 1.5, 0.2, "virginica"],
            [4.4, 2.9, 1.4, 0.2, "virginica"],
            [4.9, 3.1, 1.5, 0.1, "virginica"],
            [5.4, 3.7, 1.5, 0.2, "virginica"],
            [4.8, 3.4, 1.6, 0.2, "virginica"],
            [4.8, 3, 1.4, 0.1, "virginica"],
        ],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width", "class"],
    )
    df["class"] = df["class"].astype("category")
    df.round(2)
