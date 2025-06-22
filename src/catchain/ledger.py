import json
from pathlib import Path
from datetime import datetime, timezone

LEDGER_DIR_NAME = ".catchain"
LEDGER_FILE_NAME = "ledger.json"


def init_project(base_dir: Path = Path(".")) -> None:
    """
    Initializes the ledger system in the specified directory.

    Creates a .catchain directory with an empty ledger.json file if they
    do not already exist.

    Args:
        base_dir: The base directory of the project. Defaults to current dir.
    """
    ledger_dir = base_dir / LEDGER_DIR_NAME
    ledger_file = ledger_dir / LEDGER_FILE_NAME

    if ledger_dir.exists() and ledger_file.exists():
        print("Project already initialized.")
        return

    ledger_dir.mkdir(exist_ok=True)

    if not ledger_file.exists():
        with open(ledger_file, "w") as f:
            json.dump([], f)
        print(f"Initialized empty ledger at {ledger_file}")


def add_entry(dataset_hash: str, source_uri: str, base_dir: Path = Path(".")) -> None:
    """
    Adds a new dataset provenance entry to the ledger.

    Args:
        dataset_hash: The SHA-256 hash of the dataset.
        source_uri: The source location of the data (e.g., a file path or S3 URI).
        base_dir: The base directory of the project.
    """
    ledger_file = base_dir / LEDGER_DIR_NAME / LEDGER_FILE_NAME
    if not ledger_file.exists():
        raise FileNotFoundError("Ledger not found. Please run 'catchain init' first.")

    with open(ledger_file, "r+") as f:
        entries = json.load(f)

        new_entry = {
            "hash": dataset_hash,
            "source_uri": source_uri,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "transformations": [],
        }

        entries.append(new_entry)

        f.seek(0)
        json.dump(entries, f, indent=4)
