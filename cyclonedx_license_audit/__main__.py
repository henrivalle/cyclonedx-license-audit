import argparse
import json
from pathlib import Path
import sys

from . import audit


def main():
    parser = argparse.ArgumentParser(description="Check license metadata in a local CycloneDX JSON BOM.")
    parser.add_argument("bom", type=Path)
    parser.add_argument("--include-root", action="store_true", help="also inspect metadata.component")
    parser.add_argument("--fail-on-missing", action="store_true", help="exit 1 if a component has no usable metadata")
    args = parser.parse_args()
    try:
        rows = audit(json.loads(args.bom.read_text(encoding="utf-8-sig")), args.include_root)
    except (OSError, UnicodeError, RecursionError):
        print("Could not read the UTF-8 BOM.", file=sys.stderr)
        return 2
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    missing = sum(row["status"] != "recorded" for row in rows)
    print(json.dumps({"components": rows, "without_usable_metadata": missing}, indent=2))
    return int(args.fail_on_missing and missing > 0)


if __name__ == "__main__":
    raise SystemExit(main())
