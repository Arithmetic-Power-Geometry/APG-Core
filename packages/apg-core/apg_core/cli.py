"""Command-line interface for APG-Core."""

from __future__ import annotations

import argparse
import json
from .descriptors import descriptor_summary, local_closure_defect, local_first_order_approximation


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="apg-core",
        description="Compute core Arithmetic Power Geometry descriptors."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    desc = sub.add_parser("describe", help="Describe a positive vector using APG descriptors.")
    desc.add_argument("values", nargs="+", type=float, help="Positive real values, e.g. 3 4 5")
    desc.add_argument("--exponents", nargs="+", type=float, default=[2.5, 3.0, 4.0], help="APG exponents t >= 2")

    loc = sub.add_parser("local", help="Compute two-coordinate local closure defect and first-order approximation.")
    loc.add_argument("a", type=float)
    loc.add_argument("b", type=float)
    loc.add_argument("exponent", type=float)

    args = parser.parse_args()

    if args.command == "describe":
        print(json.dumps(descriptor_summary(args.values, exponents=args.exponents), indent=2))
    elif args.command == "local":
        result = {
            "a": args.a,
            "b": args.b,
            "exponent": args.exponent,
            "exact_local_closure_defect": local_closure_defect(args.a, args.b, args.exponent),
            "first_order_entropy_approximation": local_first_order_approximation(args.a, args.b, args.exponent),
        }
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
