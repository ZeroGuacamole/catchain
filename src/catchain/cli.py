import click
from pathlib import Path
from . import ledger, hashers


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
@click.argument("path", type=click.Path(exists=True, resolve_path=True))
def add(path: str):
    """Hashes a dataset and records its provenance."""
    target_path = Path(path)

    try:
        click.echo(f"Processing '{target_path}'...")

        with click.progressbar(
            length=1, label="Hashing data", show_percent=False, show_pos=False
        ) as bar:
            dataset_hash = hashers.generate_hash(target_path)
            bar.update(1)

        click.echo(f"  -> Calculated hash: {dataset_hash}")

        ledger.add_entry(dataset_hash, str(target_path))

        click.secho(
            f"\nSuccessfully added '{target_path.name}' to the ledger.", fg="green"
        )
        click.echo(f"Dataset Hash: {dataset_hash}")

    except FileNotFoundError as e:
        click.secho(f"Error: {e}", err=True, fg="red")
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", err=True, fg="red")


@main.command()
@click.argument("dataset_hash")
def certificate(dataset_hash: str):
    """Generates a provenance certificate for a dataset hash."""
    click.echo(f"Generating certificate for '{dataset_hash}'... (Not yet implemented)")


if __name__ == "__main__":
    main()
