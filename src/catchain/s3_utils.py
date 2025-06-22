import boto3
import tempfile
import shutil
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse


@contextmanager
def handle_s3_path(s3_uri: str):
    """
    A context manager to download S3 content to a temporary local path.

    Handles both single S3 objects and prefixes (directories). The temporary
    data is automatically cleaned up upon exiting the context.

    Args:
        s3_uri: The S3 URI (e.g., "s3://my-bucket/my-file.txt").

    Yields:
        A Path object to the temporary local file or directory.
    """
    s3 = boto3.client("s3")
    parsed_uri = urlparse(s3_uri)
    if parsed_uri.scheme != "s3":
        raise ValueError(f"Invalid S3 URI: {s3_uri}")

    bucket = parsed_uri.netloc
    key = parsed_uri.path.lstrip("/")

    temp_dir = tempfile.mkdtemp()
    try:
        # Check if the key is a "directory" (prefix)
        # We consider it a directory if the key ends with a slash or if it's a prefix for multiple objects
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=key)
        key_count = sum(len(page.get("Contents", [])) for page in pages)

        pages = paginator.paginate(Bucket=bucket, Prefix=key)

        if key.endswith("/") or key_count > 1:
            # It's a directory/prefix
            for page in pages:
                for obj in page.get("Contents", []):
                    obj_key = obj["Key"]
                    # Create subdirectories if necessary
                    relative_path = Path(obj_key).relative_to(
                        Path(key).parent if key.endswith("/") else key
                    )
                    dest_path = Path(temp_dir) / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    if not str(obj_key).endswith("/"):
                        s3.download_file(bucket, obj_key, str(dest_path))
            yield Path(temp_dir)
        elif key_count == 1:
            # It's a single file
            local_path = Path(temp_dir) / Path(key).name
            s3.download_file(bucket, key, str(local_path))
            yield local_path
        else:
            raise FileNotFoundError(f"S3 object not found at URI: {s3_uri}")

    finally:
        shutil.rmtree(temp_dir)
