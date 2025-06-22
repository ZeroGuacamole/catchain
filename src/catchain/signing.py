import gnupg
import json
from typing import Any


def canonicalize_entry(entry_data: dict[str, Any]) -> str:
    """
    Converts a dictionary into a canonical and deterministic JSON string.

    Args:
        entry_data: The dictionary to canonicalize.

    Returns:
        A compact, sorted JSON string representation of the dictionary.
    """

    def sort_dict(d: Any):
        if isinstance(d, dict):
            return {k: sort_dict(d[k]) for k in sorted(d)}
        if isinstance(d, list):
            return [sort_dict(i) for i in d]
        return d

    sorted_data = sort_dict(entry_data)

    return json.dumps(sorted_data, separators=(",", ":"))


def sign_payload(payload: str, key_id: str) -> dict[str, str]:
    """
    Signs a string payload with a specified GPG key.

    Args:
        payload: The string to sign (should be a canonical representation).
        key_id: The GPG key ID (e.g., email or fingerprint) to use for signing.

    Returns:
        A dictionary containing the signature and the key ID used.

    Raises:
        ValueError: If GPG signing fails (e.g., key not found).
    """
    gpg = gnupg.GPG()
    signed_data = gpg.sign(payload, keyid=key_id, detach=True)

    if not signed_data:
        raise ValueError(
            f"Failed to sign with GPG key '{key_id}'. Ensure the key is available and you have permissions."
        )

    return {
        "key_id": key_id,
        "signature": str(signed_data),
    }
