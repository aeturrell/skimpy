"""Command-line interface for skimpy."""

import click
import duckdb

from skimpy import skim


@click.command()
@click.version_option()
@click.argument("input")
def main(input: str) -> None:
    """The skimpy command line interface. Usage refers only to command line.

    Args:
        input (str): String of path of csv file to produce summary statistics on
    """
    # Uses CSV sniffer from duckdb
    df = duckdb.read_csv(input).to_df()
    skim(df)


if __name__ == "__main__":
    main(prog_name="skimpy")  # pragma: no cover
