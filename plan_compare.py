"""
This script compares power consumption profiles to power plans for a residential household. See 
README.md for more information. If README.md was not provided with this script please see the README
located in https://github.com/JHay0112/plan-compare/

Author: J. L. Hay
"""

import numpy as np
import argparse as ap


NUM_HEADER_ROWS = 1
NUM_COLUMNS = 25


def get_files() -> tuple[ap.FileType, ap.FileType]:
    """Parses plans and profiles file names from the command line."""

    parser = ap.ArgumentParser(
        "Plan Compare",
        description = "This program compares residential power plans for a set of power consumption\
 profiles. See the README in the program directory or https://github.com/JHay0112/plan-compare/ for\
 more details."
    )

    parser.add_argument(
        "plans_file",
        type = ap.FileType("r"),
        help = "CSV of power plans."
    )

    parser.add_argument(
        "profiles_file",
        type = ap.FileType("r"),
        help = "CSV of power consumption profiles."
    )

    args = parser.parse_args()
    return args.plans_file, args.profiles_file


def process_csv(csv: ap.FileType) -> list[tuple[str, list[float]]]:
    """Processes a plans or profiles CSV file into a list of rows."""

    lines = [line.split(",") for line in csv.readlines()]
    out = [None] * (len(lines) - NUM_HEADER_ROWS)

    assert len(lines) > NUM_HEADER_ROWS, f"{csv.name} does not have enough rows!"

    for i, line in enumerate(lines[NUM_HEADER_ROWS:]):

        assert len(line) == NUM_COLUMNS, f"Line {i+NUM_HEADER_ROWS+1} in {csv.name} does not have\
 the correct number of entries! ({len(line)}/{NUM_COLUMNS})"

        try:
            out[i] = (str(line[0]), [float(entry) for entry in line[NUM_HEADER_ROWS:]])
        except ValueError:
            print(f"Line {i+NUM_HEADER_ROWS+1} in {csv.name} contains an invalid entry!")
            exit()
        
    return out


def main():
    """Main routine"""

    plans_file, profiles_file = get_files()

    plans = process_csv(plans_file)
    plans_file.close()
    profiles = process_csv(profiles_file)
    profiles_file.close()


if __name__ == "__main__":

    try:
        main()
    except AssertionError as exception:

        print(exception.args[0])