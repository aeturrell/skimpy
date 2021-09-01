"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """skimpy."""


if __name__ == "__main__":
    main(prog_name="skimpy")  # pragma: no cover
