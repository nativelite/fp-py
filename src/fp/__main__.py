"""Command line interface for fp."""

from __future__ import annotations

import argparse
import json

from . import fingerprint, get_components


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a device fingerprint")
    parser.add_argument(
        "--components",
        action="store_true",
        help="print the raw component values instead of the hash",
    )
    args = parser.parse_args()
    if args.components:
        print(json.dumps(get_components(), indent=2, sort_keys=True))
    else:
        print(fingerprint())


if __name__ == "__main__":
    main()
