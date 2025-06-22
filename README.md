# CatChain ⛓️

**CatChain: A verifiable data supply chain for AI.**

CatChain is a command-line tool for creating and managing auditable data pipelines for AI model training. As regulators and customers increasingly demand to know how an AI model was built, data provenance—the documented history of data—is becoming critical.

This tool allows you to build a verifiable "supply chain" for your training data. It uses cryptographic hashing to create an immutable audit trail of where your data came from and when it was processed, producing a "provenance certificate" that can be linked to your trained model.

## Why CatChain?

- **Trust & Transparency:** Build confidence in your models by providing a clear, verifiable history of the training data.
- **Auditability:** Defend your model's behavior to auditors and stakeholders with a cryptographic receipt.
- **Developer-First:** A simple, fast CLI tool that integrates easily into your existing MLOps workflows.

## Installation

You can install CatChain directly from this repository using `pip`:

```bash
pip install git+https://github.com/ZeroGuacamole/catchain.git
```

**Prerequisites:**

- To use S3 URIs, you will need to have your AWS credentials configured in your environment.
- To use the `--sign` feature, you must have `gpg` installed and a GPG key available on your system.

## Quick Start

Here is a complete workflow for generating your first provenance certificate, including tracking a transformation.

### 1. Initialize Your Project

Navigate to your project's root directory and run `init`. This creates a hidden `.catchain` directory to store your data ledger.

```bash
catchain init
```

> ✨ Initialized empty ledger at .catchain/ledger.json

### 2. Add a Raw Dataset

Add your initial, raw dataset to the ledger. CatChain will hash the data and record its metadata. You can optionally sign the entry with your GPG key ID.

**Local File:**

```bash
catchain add ./data/raw_dataset.csv --sign your.email@example.com
```

**S3 Directory:**

```bash
catchain add s3://my-ai-bucket/datasets/raw_images/ --sign FINGERPRINT
```

The output will give you a unique, deterministic hash for your dataset.

> ✅ Successfully added './data/raw_dataset.csv' to the ledger.
>
> **Dataset Hash:** a5adec84d60be012f968f16e2eb410ffcc581760fb589478c30e08d3f60c0306

### 3. Transform Your Dataset

After you run a script to clean, filter, or augment your data, you create a new version. Use the `transform` command to add this new version to the ledger, creating a verifiable link to its parent.

```bash
catchain transform ./data/cleaned_dataset.csv \
    --from-hash a5adec84d60be012f968f16e2eb410ffcc581760fb589478c30e08d3f60c0306 \
    --description "Removed rows with null values." \
    --sign your.email@example.com
```

> ✅ Successfully added './data/cleaned_dataset.csv' to the ledger.
>
> **Dataset Hash:** 75970c0ce13e3b27fc183e99f1ff2d5b586153ea4951b879de38fbcdb3c2e268

### 4. Generate the Provenance Certificate

Using the hash of your final, transformed dataset, generate the certificate.

```bash
catchain certificate 75970c0ce13e3b27fc183e99f1ff2d5b586153ea4951b879de38fbcdb3c2e268 --output provenance.json
```

> ✅ Successfully saved certificate to provenance.json

This creates a `provenance.json` file that contains the full history of your data.

## The Provenance Certificate

The generated certificate is a self-contained, verifiable JSON document. The inclusion of `lineage` and `signature` blocks provides a powerful, auditable history.

```json
{
  "schema_version": "1.0.0",
  "dataset_hash": "75970c0ce13e3b27fc183e99f1ff2d5b586153ea4951b879de38fbcdb3c2e268",
  "hash_algorithm": "sha256",
  "provenance": {
    "source_uri": "file:///path/to/your/project/data/cleaned_dataset.csv",
    "timestamp_utc": "2025-06-22T17:22:35.417103+00:00",
    "lineage": {
      "parent_hash": "a5adec84d60be012f968f16e2eb410ffcc581760fb589478c30e08d3f60c0306",
      "transform_description": "Removed rows with null values."
    }
  },
  "signature": {
    "key_id": "your.email@example.com",
    "signature": "-----BEGIN PGP SIGNATURE-----\\n\\niQIzBAABCAAdFiEE...\\n-----END PGP SIGNATURE-----\\n"
  }
}
```

## Linking Certificate to a Model

The `provenance.json` file is the verifiable link between your model and its data. To complete the chain, you should upload this certificate alongside your model to a model repository like Hugging Face.

By placing the `provenance.json` file in your Hugging Face model repository, you create a public, auditable record that anyone can use to verify the exact dataset that was used to train that specific model.
