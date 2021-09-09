"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from skimpy import __main__
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
