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

You will also need to have your AWS credentials configured in your environment to use S3 URIs.

## Quick Start

Here is a complete workflow for generating your first provenance certificate.

### 1. Initialize Your Project

Navigate to your project's root directory and run `init`. This creates a hidden `.catchain` directory to store your data ledger.

```bash
catchain init
```

> ✨ Initialized empty ledger at .catchain/ledger.json

### 2. Add a Dataset

Add a dataset (a file or a directory) to the ledger. CatChain will hash the data and record its metadata. This works for both local paths and S3 URIs.

**Local File:**

```bash
catchain add ./data/my_training_data.csv
```

**S3 Directory:**

```bash
catchain add s3://my-ai-bucket/datasets/images/
```

The output will give you a unique, deterministic hash for your dataset.

> ✅ Successfully added 's3://my-ai-bucket/datasets/images/' to the ledger.
>
> **Dataset Hash:** 2b89a3cce3818f769d95c45e612f04e43f076b66494791a8379659a72b834d85

### 3. Generate the Provenance Certificate

Using the hash from the previous step, generate the certificate.

```bash
catchain certificate 2b89a3cce3818f769d95c45e612f04e43f076b66494791a8379659a72b834d85 --output provenance.json
```

> ✅ Successfully saved certificate to provenance.json

This creates a `provenance.json` file in your directory.

## Linking Certificate to a Model

The `provenance.json` file is the verifiable link between your model and its data. To complete the chain, you should upload this certificate alongside your model to a model repository like Hugging Face.

By placing the `provenance.json` file in your Hugging Face model repository, you create a public, auditable record that anyone can use to verify the exact dataset that was used to train that specific model.
