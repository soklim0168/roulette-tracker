"""Simple command-line interface for the roulette tracker."""

import argparse
import json

from src.analyzer import RouletteAnalyzer


def main() -> None:
    parser = argparse.ArgumentParser(description="Record roulette spins and inspect statistics.")
    parser.add_argument("--spin", type=int, action="append", help="Record a number (repeat for multiple spins)")
    parser.add_argument("--min-spins", type=int, default=100, help="Minimum spins for bias testing")
    parser.add_argument("--report", action="store_true", help="Print the bias report")
    args = parser.parse_args()

    analyzer = RouletteAnalyzer(min_spins=args.min_spins)
    for number in args.spin or []:
        analyzer.add_spin(number)
    output = analyzer.detect_bias() if args.report else analyzer.get_statistics()
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
