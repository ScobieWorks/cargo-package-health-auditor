import argparse
import json
import pathlib
import sys

from .audit import audit_workspace

def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit Rust workspace metadata completeness.")
    parser.add_argument(
        "workspace_root",
        nargs="?",
        default=".",
        help="Path to the Cargo workspace root (default: current directory).",
    )
    args = parser.parse_args(argv)
    root = pathlib.Path(args.workspace_root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    reports = audit_workspace(root)
    json.dump(reports, sys.stdout, indent=2)
    print()

if __name__ == "__main__":
    main()
