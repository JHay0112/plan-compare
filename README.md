# Plan Compare

This script compares power plans for a residential site. It expects two CSV files as inputs like so

```sh
python plan_compare.py plans.csv profiles.csv
```

The `plans.csv` file is the set of power plans for consideration and has a header of the form

```csv
Plan, Fee, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
```

Each row contined in `plans.csv` is a power plan and its cost per unit electricity for each hour in 
a day. The `Plan` column uniquely identifies each plan, the `Fee` column identifies any daily 
charges, and the following enumerated columns have a decimal value indicating the cost per unit of 
electricity consumed during that hour. This permits that the tool cope with fluctations in cost from
a power retailer over the course of one day. There is no function that lets this tool deal with 
rvariations between days.

The `profiles.csv` file is a set of power consumption profiles and their power consumption per hour.
For example, different profiles may exist for power consumption on a winters day, when heaters are 
likely to be used, and for a summers day, where heating is not needed. The header of `profiles.csv` 
takes the form

```csv
Profile, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
```

Each row in `profiles.csv` is a power profile and its consumption for each hour in a day. The 
`Profile` column uniquely identifies each profile, and the following enumerated columns have a 
decimal value indicating the amount of electricity typically consumed in that hour. The electricity
consumption values should indicate the number of units of electricity typically consumed in that
hour.

When supplied with the details of power plans and consumption profiles the tool evaluates all plans
against each profile. The results are then output to the terminal. For each profile, the tool will
list the power plans in order of cheapest to most expensive and give the score associated with each
plan.