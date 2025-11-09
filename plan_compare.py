"""
This script compares power consumption profiles to power plans for a residential household. See 
README.md for more information. If README.md was not provided with this script please see the README
located in https://github.com/JHay0112/plan-compare/

Author: J. L. Hay
"""

import numpy as np
import argparse as ap
from dataclasses import dataclass


NUM_HEADER_ROWS = 1
PLANS_NUM_COLUMNS = 27
PROFILES_NUM_COLUMNS = 26


@dataclass
class Plan:
    daily_charge: float = None
    weekday_costs: list[float] = None
    weekend_costs: list[float] = None

@dataclass
class Profile:
    weekday_usage: list[float] = None
    weekend_usage: list[float] = None


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


def process_plans(plans_filename: str) -> dict[str, Plan]:
    """Processes plans from the CSV."""

    try:
        plans_file = open(plans_filename)
    except FileNotFoundError:
        print(f"{plans_filename} does not exist!")
        exit()

    plans_raw = process_csv(plans_file, PLANS_NUM_COLUMNS, NUM_HEADER_ROWS)
    plans = {}

    plans_file.close()

    for i, plan in enumerate(plans_raw):

        try:
            name, days, fee, prices = plan[0], plan[1], float(plan[2]), [float(price) for price in plan[3:]]
        except ValueError:
            print(f"Invalid value on line {i+2} in {plans_filename}!")

        plan = plans.get (name, Plan())
        if days == "All":
            plan.daily_charge = fee
            plan.weekday_costs = prices
            plan.weekend_costs = prices
        elif days == "Weekdays":
            plan.daily_charge = fee
            plan.weekday_costs = prices
        elif days == "Weekends":
            plan.daily_charge = fee
            plan.weekend_costs = prices
        else:
            raise ValueError("Unrecognised key for value \"days\".")
        plans[name] = plan

    for plan in plans.values():
        assert plan.daily_charge is not None
        assert plan.weekday_costs is not None
        assert plan.weekend_costs is not None

    return plans


def process_profiles(profiles_filename: str) -> dict[str, Profile]:
    """Processes profiles from the CSV."""

    try:
        profiles_file = open(profiles_filename)
    except FileNotFoundError:
        print(f"{profiles_filename} does not exist!")
        exit()

    profiles_raw = process_csv(profiles_file, PROFILES_NUM_COLUMNS, NUM_HEADER_ROWS)
    profiles = {}

    profiles_file.close()

    for i, profile in enumerate(profiles_raw):

        try:
            name, days, prices = profile[0], profile[1], [float(price) for price in profile[2:]]
        except ValueError:
            print(f"Invalid value on line {i+2} in {profiles_filename}!")

        profile = profiles.get (name, Profile())
        if days == "All":
            profile.weekday_usage = prices
            profile.weekend_usage = prices
        elif days == "Weekdays":
            plan.weekday_usage = prices
        elif days == "Weekends":
            plan.weekend_usaeg = prices
        else:
            raise ValueError("Unrecognised key for value \"days\".")
        profiles[name] = profile

    for profile in profiles.values():
        assert profile.weekday_usage is not None
        assert profile.weekend_usage is not None

    return profiles


def main():
    """Main routine"""

    plans_filename, profiles_filename = get_files()

    plans = process_plans(plans_filename)
    profiles = process_profiles(profiles_filename)

    for profile_name, profile in profiles.items():

        print(f">>> {profile_name}")
        scores = {}

        for plan_name, plan in plans.items():
            scores[plan_name] = \
                7 * plan.daily_charge + \
                5 * np.sum(np.array(plan.weekday_costs) * np.array(profile.weekday_usage)) + \
                2 * np.sum(np.array(plan.weekend_costs) * np.array(profile.weekday_usage))

        scores = dict(sorted(scores.items(), key=lambda x: x[1]))

        for plan_name, score in scores.items():
            print(f"{plan_name:<50} {score:>10.3f}")

        print(f"<<< {profile_name}")


if __name__ == "__main__":

    try:
        main()
    except AssertionError as exception:

        print(exception.args[0])