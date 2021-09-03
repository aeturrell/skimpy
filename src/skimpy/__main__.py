"""Command-line interface."""
import click
import pandas as pd

from skimpy import skimpy


@click.command()
@click.version_option()
@click.argument("input")
def main(input) -> None:
    """skimpy."""
    df = pd.read_csv(input, infer_datetime_format=True, parse_dates=True)
    df = df.infer_objects()
    skimpy(df)


if __name__ == "__main__":
    main(prog_name="skimpy")  # pragma: no cover
