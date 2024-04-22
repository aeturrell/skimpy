"""Command-line interface for skimpy."""

import click
import pandas as pd

from skimpy import skim


@click.command()
@click.version_option()
@click.argument("input")
def main(input) -> None:
    """The skimpy command line interface. Usage refers only to command line.

    Args:
        input ([csv]): A csv file to produce summary statistics on
    """
    df = pd.read_csv(input, parse_dates=True)
    df = df.infer_objects()
    skim(df)


if __name__ == "__main__":
    main(prog_name="skimpy")  # pragma: no cover
