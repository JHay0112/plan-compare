"""
This script compares power consumption profiles to power plans for a residential household. See 
README.md for more information. If README.md was not provided with this script please see the README
located in https://github.com/JHay0112/plan-compare/

Author: J. L. Hay
"""

import numpy as np
import argparse as ap


NUM_HEADER_ROWS = 1
PLANS_NUM_COLUMNS = 26
PROFILES_NUM_COLUMNS = 25


def get_files() -> tuple[ap.FileType, ap.FileType]:
    """Parses plans and profiles file names from the command line."""

    parser = ap.ArgumentParser(
        "Plan Compare",
        description = "This program compares residential power plans for a set of power consumption\
 profiles. See the README in the program directory or https://github.com/JHay0112/plan-compare/ for\
 more details."
    )

    parser.add_argument(
        "plans_filename",
        type = str,
        help = "CSV of power plans."
    )

    parser.add_argument(
        "profiles_filename",
        type = str,
        help = "CSV of power consumption profiles."
    )

    args = parser.parse_args()
    return args.plans_filename, args.profiles_filename


def process_csv(csv: ap.FileType, columns: int, header_rows: int) -> list[list[str]]:
    """Processes a CSV into a list of rows."""

    lines = [line.split(",") for line in csv.readlines()]
    out = [None] * (len(lines) - header_rows)

    assert len(lines) > header_rows, f"{csv.name} does not have enough rows!"

    for i, line in enumerate(lines[header_rows:]):

        assert len(line) == columns, f"Line {i+header_rows+1} in {csv.name} does not have the\
 correct number of entries! ({len(line)} != {columns})"

        out[i] = [entry for entry in line]
        
    return out


def main():
    """Main routine"""

    plans_filename, profiles_filename = get_files()

    try:
        plans_file = open(plans_filename)
    except FileNotFoundError:
        print(f"{plans_filename} does not exist!")
        exit()

    try:
        profiles_file = open(profiles_filename)
    except FileNotFoundError:
        print(f"{profiles_filename} does not exist!")
        exit()

    plans = process_csv(plans_file, PLANS_NUM_COLUMNS, NUM_HEADER_ROWS)
    profiles = process_csv(profiles_file, PROFILES_NUM_COLUMNS, NUM_HEADER_ROWS)

    plans_file.close()
    profiles_file.close()

    for i, plan in enumerate(plans):

        try:
            name, fee, prices = plan[0], float(plan[1]), float(plan[2:])
        except ValueError:
            print(f"Invalid value on line {i+2} in {plans_filename}!")
        


if __name__ == "__main__":

    try:
        main()
    except AssertionError as exception:

        print(exception.args[0])