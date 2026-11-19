# Cargo Package Health Auditor

A lightweight, offline CLI that audits Rust workspaces for essential metadata such as README files, LICENSE files, and SPDX license identifiers. It recursively scans all `Cargo.toml` files in a workspace and reports any missing or mismatched information in JSON format, making it easy to integrate into CI pipelines or local development workflows.

## Features

- Detects missing `README.md`, `README.rst`, or `README.txt` files.
- Checks for the presence of a `LICENSE` or `LICENSE-*` file.
- Parses the `[package]` section of `Cargo.toml` to ensure a `license` field exists and matches a known SPDX identifier.
- Optionally verifies that the license file contains the SPDX short identifier.
- Outputs a concise JSON report that can be consumed by CI scripts or local developers.

## Installation

```bash
pip install git+https://github.com/ScobieWorks/cargo-package-health-auditor.git
```

## Usage

```bash
cargo-package-health-auditor <workspace-root>
```

The command prints a JSON report to stdout. You can redirect it to a file or pipe it into other tools.

## License

MIT License

## Limitations
<!-- generated-limitations:b57c491b382ffef7cbcbe45f304d09de757f9da0d9f6ebb78dfecf5ba15e92d5 -->
- The file-discovery scan in `src/cargo_package_health_auditor/audit.py` selects `Cargo.toml`; nonmatching filenames are outside that scan.
- The text reader in `src/cargo_package_health_auditor/audit.py` uses UTF-8; supply UTF-8 text for that reading path. Invalid UTF-8 bytes are ignored.
<!-- /generated-limitations -->
