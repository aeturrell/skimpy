"""Command-line interface for skimpy."""

import pathlib

import click
import duckdb
import pandas as pd

from skimpy import skim


@click.command()
@click.version_option()
@click.argument("input")
@click.option(
    "--table",
    "-t",
    default=None,
    help="Table name (required for sqlite files). If not provided, shows available tables.",
)
def main(input: str, table: str | None) -> None:
    """The skimpy command line interface. Usage refers only to command line.

    Args:
        input (str): Path of data file (csv, parquet, or sqlite)
        table (str | None): Table name for sqlite files; shows available tables if not provided
    """
    df = _load_data_from_file(input, table)
    skim(df)


def _load_data_from_file(input: str, table: str | None = None) -> pd.DataFrame:
    """Load data from a file based on its extension.

    Args:
        input: Path to CSV, parquet, or SQLite file
        table: Optional table name for SQLite files

    Returns:
        pandas DataFrame loaded from the specified file

    Raises:
        ValueError: If file extension is not supported or required arguments are missing
    """
    input_path = pathlib.Path(input)
    if not input_path.exists():
        msg = f"Input path does not exist: {input}"
        raise FileNotFoundError(msg)

    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        return duckdb.read_csv(str(input_path)).to_df()

    if suffix == ".parquet":
        return duckdb.read_parquet(str(input_path)).to_df()

    if suffix == ".sqlite":
        _handle_sqlite_file(str(input_path), table)
        # Use ATTACH to load from SQLite database
        df = duckdb.sql(f"ATTACH '{input}' AS mydb; SELECT * FROM mydb.{table}").to_df()
        return df

    msg = f"Unsupported file type: {suffix}. Supported types: .csv, .parquet, .sqlite"
    raise ValueError(msg)


def _handle_sqlite_file(sqlite_path: str, table: str | None) -> None:
    """Handle SQLite file loading and validation.

    Args:
        sqlite_path: Path to the SQLite database file
        table: Optional table name to load; if None, shows available tables

    Raises:
        ValueError: If no table is provided for a non-empty SQLite database
    """
    con = duckdb.connect(sqlite_path)
    available_tables = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    if not available_tables:
        msg = "SQLite database contains no tables."
        raise ValueError(msg)

    table_names = [t[0] for t in available_tables]

    if not table:
        print(f"Available tables in {sqlite_path}:")
        for t in table_names:
            print(f"  - {t}")
        msg = "Please specify a table using --table NAME or -t NAME (e.g., skimpy your_db.sqlite -t my_table)"
        raise ValueError(msg)

    if table not in table_names:
        msg = f'Table "{table}" not found in {sqlite_path}. Available tables: {", ".join(table_names)}'
        raise ValueError(msg)

    con.close()


if __name__ == "__main__":
    main(prog_name="skimpy")  # pragma: no cover
