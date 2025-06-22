import click
from pathlib import Path
from . import ledger, hashers
from .s3_utils import handle_s3_path


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
@click.argument("path", type=str)
def add(path: str):
    """Hashes a local or S3 dataset and records its provenance."""
    try:
        if path.startswith("s3://"):
            # Handle S3 path
            click.echo(f"Processing S3 URI '{path}'...")
            with handle_s3_path(path) as local_path:
                process_and_record(local_path, source_uri=path)
        else:
            # Handle local path
            target_path = Path(path).resolve()
            if not target_path.exists():
                raise FileNotFoundError(f"Local path does not exist: {target_path}")
            click.echo(f"Processing '{target_path}'...")
            process_and_record(target_path, source_uri=target_path.as_uri())

    except FileNotFoundError as e:
        click.secho(f"Error: {e}", err=True, fg="red")
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", err=True, fg="red")


def process_and_record(local_path: Path, source_uri: str):
    """Helper function to hash data and record it in the ledger."""
    with click.progressbar(
        length=1, label="Hashing data", show_percent=False, show_pos=False
    ) as bar:
        dataset_hash = hashers.generate_hash(local_path)
        bar.update(1)

    click.echo(f"  -> Calculated hash: {dataset_hash}")

    ledger.add_entry(dataset_hash, source_uri)

    click.secho(f"\nSuccessfully added '{source_uri}' to the ledger.", fg="green")
    click.echo(f"Dataset Hash: {dataset_hash}")


@main.command()
@click.argument("dataset_hash")
def certificate(dataset_hash: str):
    """Generates a provenance certificate for a dataset hash."""
    click.echo(f"Generating certificate for '{dataset_hash}'... (Not yet implemented)")


if __name__ == "__main__":
    main()
