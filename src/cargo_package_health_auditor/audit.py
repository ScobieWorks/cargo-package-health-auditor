import pathlib
import tomllib
from typing import Any, Dict, List

# A small set of common SPDX identifiers. Extend as needed.
KNOWN_SPDX = {
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "LGPL-3.0-or-later",
    "GPL-3.0-or-later",
    "LGPL-2.1-or-later",
    "GPL-2.0-or-later",
    "CC0-1.0",
    "Unlicense",
}


def audit_workspace(root: pathlib.Path) -> List[Dict[str, Any]]:
    """Audit all crates in a Cargo workspace.

    Parameters
    ----------
    root: pathlib.Path
        Path to the workspace root.

    Returns
    -------
    List[Dict[str, Any]]
        A list of per-crate audit reports.
    """
    reports: List[Dict[str, Any]] = []
    for cargo_toml in root.rglob("Cargo.toml"):
        crate_dir = cargo_toml.parent
        report: Dict[str, Any] = {"crate_path": str(crate_dir.relative_to(root))}

        # README check
        readme_present = any((crate_dir / f"README.{ext}").exists() for ext in ("md", "rst", "txt"))
        report["readme_present"] = readme_present

        # License file check
        license_file = None
        # First look for a plain LICENSE file
        candidate = crate_dir / "LICENSE"
        if candidate.exists():
            license_file = candidate
        else:
            # Look for LICENSE-* variants
            for p in crate_dir.iterdir():
                if p.name.startswith("LICENSE-") and p.is_file():
                    license_file = p
                    break
        license_file_present = license_file is not None
        report["license_file_present"] = license_file_present

        # Parse Cargo.toml
        try:
            with cargo_toml.open("rb") as f:
                data = tomllib.load(f)
        except Exception:
            data = {}
        package = data.get("package", {})
        license_field = package.get("license")
        license_field_present = license_field is not None
        report["license_field_present"] = license_field_present
        license_field_valid = license_field_present and license_field in KNOWN_SPDX
        report["license_field_valid"] = license_field_valid

        # Check that the license file contains the SPDX identifier
        license_file_contains_spdx = False
        if license_file_present and license_field_valid:
            try:
                content = license_file.read_text(encoding="utf-8", errors="ignore")
                license_file_contains_spdx = license_field in content
            except Exception:
                license_file_contains_spdx = False
        report["license_file_contains_spdx"] = license_file_contains_spdx

        reports.append(report)
    return reports
