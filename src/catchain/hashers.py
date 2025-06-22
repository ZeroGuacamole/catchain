import hashlib
from pathlib import Path


def hash_file(path: Path) -> str:
    """
    Computes the SHA-256 hash of a single file.

    Args:
        path: The path to the file.

    Returns:
        The hex-encoded SHA-256 hash of the file's content.
    """
    hasher = hashlib.sha256()
    # Read in 64k chunks to handle large files efficiently
    chunk_size = 65536

    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()


def hash_directory(path: Path) -> str:
    """
    Computes a deterministic SHA-256 hash for a directory's contents.

    The hash is derived from a sorted list of relative file paths and their
    individual SHA-256 hashes. This ensures the final hash is consistent
    regardless of the filesystem's ordering.

    Args:
        path: The path to the directory.

    Returns:
        The hex-encoded SHA-256 hash representing the directory's state.
    """
    if not path.is_dir():
        raise ValueError("Path must be a directory.")

    hashes = []
    for item in sorted(path.rglob("*")):
        if item.is_file():
            relative_path = item.relative_to(path)
            file_hash = hash_file(item)
            hashes.append(f"{relative_path}:{file_hash}")

    # Hash the concatenated string of "path:hash" records
    dir_hasher = hashlib.sha256()
    dir_hasher.update("".join(hashes).encode("utf-8"))

    return dir_hasher.hexdigest()


def generate_hash(path: Path) -> str:
    """
    Generates a SHA-256 hash for a given file or directory path.

    Automatically determines whether the path is a file or a directory and
    calls the appropriate hashing function.

    Args:
        path: The path to the file or directory.

    Returns:
        The resulting SHA-256 hash.

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"No such file or directory: {path}")

    if path.is_dir():
        return hash_directory(path)
    else:
        return hash_file(path)
