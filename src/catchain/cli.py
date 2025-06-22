import click
from . import ledger


@click.group()
def main():
    """
    CatChain: A tool for creating verifiable data supply chains for AI.
    """
    pass


@main.command()
def init():
    """Initializes a new CatChain project in the current directory."""
    try:
        ledger.init_project()
    except Exception as e:
        click.echo(f"Error initializing project: {e}", err=True)


@main.command()
@click.argument("path", type=click.Path(exists=True))
def add(path: str):
    """Hashes a dataset and records its provenance."""
    click.echo(f"Hashing and adding '{path}' to the ledger... (Not yet implemented)")


@main.command()
@click.argument("dataset_hash")
def certificate(dataset_hash: str):
    """Generates a provenance certificate for a dataset hash."""
    click.echo(f"Generating certificate for '{dataset_hash}'... (Not yet implemented)")


if __name__ == "__main__":
    main()
