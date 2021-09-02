"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from skimpy import __main__
from skimpy import generate_test_data
from skimpy import skimpy


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
    """[summary]."""
    df = generate_test_data()
    skimpy(df)
