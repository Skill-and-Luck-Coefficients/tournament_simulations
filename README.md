# Tournament Simulations
Repository dedicated to tournament simulations.

## **How to use it**

- [Source Code](https://github.com/EstefanoB/tournament_simulations)

### **Dependencies**

Python version: 3.10

- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)

### **Virtual Environments**

Pip

```
$ python3 -m venv env                           # create env
$ source env/bin/activate                       # activate env
$ python3 -m pip install -r requirements.txt    # install packages
```

Conda

```
$ conda env create -f environment.yml  # create env with all packages
$ conda activate scrape_matches        # activate env
```

**Remark**: `tournament_simulations` is the main folder, so you should run from the same directory
you found this file after cloning the repository:

```
$ cd tournament_simulations
```

**Note**: If you want to use this as a package, after installing all required packages you should go to where this file is and run:

```
$ python3 -m pip install .
```

## Installation from sources
In the same directory you found this file after cloning the repository, execute:

```
$ python3 -m pip install --upgrade build
$ python3 -m build
```

For more information, see [Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

Then, you can activate your virtual environment and run

```
$ python3 -m pip install dist/*.whl
```

or run

```
$ python3 -m pip install -e dist/*.whl
```

for installing in [development mode](https://pip.pypa.io/en/latest/cli/pip_install/#install-editable)

You can also install optional packages:

```
$ python3 -m pip install ".[test]"      # packages for training
$ python3 -m pip install ".[notebook]"  # packages for jupyter notebooks
$ python3 -m pip install ".[lint]"      # packages for linting
```

<br>

## **API**
---

Notebook examples for all main classes/methods can be found in `src/example_notebooks/`. 

Their checkpoins have also been pushed to GitHub, so you can just take a look before cloning/installing this project.

### **Data Structures**

There are two main pandas.DataFrame structures used in this project.

- `data_structues.Matches`
    - Stores tournament matches: tournament name, date, home-team, away-team, winner, etc..
    - Definition/documentation in `src/tournament_simulations/data_structures/matches/matches.py`
- `data_structues.PointsPerMatch`
    - Stores how many points a team gained all matches played (each one is a separate dataframe row).
    - Definition/documentation in `src/tournament_simulations/data_structures/points_per_match/points_per_match.py/PointsPerMatch`

### **Result Simulations**

Simulate results given one of the data structures ([Data Structures](#data-structures)).

Simulations can be tournament-wide or match-wide:

- **tournament-wide**: All matches in a tournament will use the same probability tuple, i.e., (probability home team win, probability draw, probability away team win).

- **match_wide**: Each match should have its own probability tuple.

Classes:

- `simulations.SimulateMatches`: simulate `data_structues.Matches`
    - Contains methods for both types of simulations: `.tournament_wide(...)` and `.match_wide(...)`
    - Definition/documentation in `src/tournament_simulations/simulations/simulate_matches.py`
- `simualtions.SimulatePointsPerMatch`: simulate `data_structues.PointsPerMatch`
    - Contains methods for both types of simulations: `.tournament_wide(...)` and `.match_wide(...)`
    - Definition/documentation in `src/tournament_simulations/simulations/simulate_points_per_match.py`

### **Round-Robin Schedule Creation**

Given either the number of teams or a list of team names, creates a random single/double round-robin scheduler. It can create long tournaments by concatenating round-robin schedules together.

- `schedules.round_robin.SingleRoundRobin`
    - Contains a method to create long tournaments: `.get_full_schedule(...)`
    - Definition/documentation in `src/tournament_simulations/schedules/round_robin/single_round_robin.py`
- `schedules.round_robin.DoubleRoundRobin`
    - Contains a method to create long tournaments: `.get_full_schedule(...)`
    - Definition/documentation in`src/tournament_simulations/schedules/round_robin/double_round_robin.py`

### **Tournaments Permutations**

Permute tournament matches (Matches [data structure](#data-structures)) following a double-round robin schedule.

- `schedules.permutation.MatchesPermutations`
    - Contains a method to create n permutations: `.create_n_permutations(...)`
    - Definition/documentation in `src/tournament_simulations/schedules/permutation/matches_permutations.py`

## **Logs**

By default, everything is logged to `tournament_simulations_logs.log` located in whatever your current working directory is. 
Severity level can be changed in `src/logs/logs.py`. By default it is `logging.WARNING`.

## **Licensing**
---

This repository is licensed under the Apache License, Version 2.0. See LICENSE for the full license text.
