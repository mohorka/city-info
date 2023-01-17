"""CLI for viewing city information."""
import argparse
import sys

import pandas as pd

from . import get_city_info


def main() -> int:
    """Entry point for the application."""
    parser = argparse.ArgumentParser(
        prog="python3 -m city_info",
        description="Get information about a city for a given year.",
    )
    parser.add_argument("data_file", help="Path to the data file")
    parser.add_argument("city", help="Name of the city")
    parser.add_argument("year", help="Year to get data for", type=int)
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.data_file, parse_dates=["dt"])
    except IsADirectoryError as e:
        print(f"Provided path {args.data_file} is a directory: {e}.", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Can't access file {args.data_file}: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"File {args.data_file} not found: {e}.", file=sys.stderr)
        return 1

    try:
        city_info = get_city_info(df, args.city, args.year)
    except KeyError:
        print(f"csv file {args.data_file} does not contain the expected columns.")
        return 1
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unknown error: {e}", file=sys.stderr)
        return 1

    print(f"Min temp: {city_info.min_temp}")
    print(f"Max temp: {city_info.max_temp}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
