import pandas as pd

_df_data_mw = {
    "id": [
        "deterministic",
        "deterministic",
        "deterministic",
        "deterministic",
        "deterministic",
        "deterministic",
        "uniformly_random",
        "uniformly_random",
        "uniformly_random",
        "uniformly_random",
        "uniformly_random",
        "uniformly_random",
    ],
    "date number": [
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        2,
        2,
    ],
    "home": [
        "A",
        "B",
        "A",
        "B",
        "A",
        "A",
        "one",
        "two",
        "two",
        "one",
        "three",
        "three",
    ],
    "away": [
        "B",
        "A",
        "B",
        "A",
        "B",
        "B",
        "three",
        "one",
        "three",
        "two",
        "two",
        "one",
    ],
    "winner": [
        "h",
        "a",
        "a",
        "d",
        "a",
        "h",
        "a",
        "h",
        "a",
        "h",
        "h",
        "a",
    ],
}

matches_df_mw = pd.DataFrame(_df_data_mw).set_index(["id", "date number"])


_matches_to_prob = {
    "probabilities_result": [
        {"3-0": 1, "1-1": 0, "1-3": 0},
        {"3-0": 0, "1-1": 1, "1-3": 0},
        {"3-0": 1, "1-1": 0, "1-3": 0},
        {"3-0": 0, "1-1": 0, "1-3": 1},
        {"3-0": 0, "1-1": 0, "1-3": 1},
        {"3-0": 1, "1-1": 0, "1-3": 0},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
        {"2-1": 0.333, "1-1": 0.333, "1-2":  0.334},
    ],
    "probabilities_winner": [
        {"h": 1, "d": 0, "a": 0},
        {"h": 0, "d": 1, "a": 0},
        {"h": 1, "d": 0, "a": 0},
        {"h": 0, "d": 0, "a": 1},
        {"h": 0, "d": 0, "a": 1},
        {"h": 1, "d": 0, "a": 0},
        {"h": 0.333, "d": 0.333, "a":  0.334},
        {"h": 0.333, "d": 0.333, "a":  0.334},
        {"h": 0.333, "d": 0.333, "a":  0.334},
        {"h": 0.333, "d": 0.333, "a":  0.334},
        {"h": 0.333, "d": 0.333, "a":  0.334},
        {"h": 0.333, "d": 0.333, "a":  0.334},
    ],
    "probabilities_ppm_310": [
        {(3, 0): 1, (1, 1): 0, (0, 3): 0},
        {(3, 0): 0, (1, 1): 1, (0, 3): 0},
        {(3, 0): 1, (1, 1): 0, (0, 3): 0},
        {(3, 0): 0, (1, 1): 0, (0, 3): 1},
        {(3, 0): 0, (1, 1): 0, (0, 3): 1},
        {(3, 0): 1, (1, 1): 0, (0, 3): 0},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
        {(3, 0): 0.333, (1, 1): 0.333, (0, 3):  0.334},
    ],
    "probabilities_ppm_201": [
        {(2, 1): 1, (0, 0): 0, (1, 2): 0},
        {(2, 1): 0, (0, 0): 1, (1, 2): 0},
        {(2, 1): 1, (0, 0): 0, (1, 2): 0},
        {(2, 1): 0, (0, 0): 0, (1, 2): 1},
        {(2, 1): 0, (0, 0): 0, (1, 2): 1},
        {(2, 1): 1, (0, 0): 0, (1, 2): 0},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
        {(2, 1): 0.333, (0, 0): 0.333, (1, 2):  0.334},
    ],
}

matches_to_probabilities = pd.DataFrame(_matches_to_prob, index=matches_df_mw.index)


_df_data_tw = {
    "id": [
        "always_home_win",
        "always_home_win",
        "always_draw",
        "always_draw",
        "always_away_win",
        "always_away_win",
        "uniform_prob",
        "uniform_prob",
        "uniform_prob",
        "uniform_prob",
        "uniform_prob",
        "uniform_prob",
    ],
    "date number": [
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        2,
        2,
    ],
    "home": [
        "home",
        "home",
        "home",
        "home",
        "home",
        "home",
        "one",
        "two",
        "two",
        "one",
        "three",
        "three",
    ],
    "away": [
        "away",
        "away",
        "away",
        "away",
        "away",
        "away",
        "three",
        "one",
        "three",
        "two",
        "two",
        "one",
    ],
    "winner": [
        "h",
        "h",
        "d",
        "d",
        "a",
        "a",
        "d",
        "d",
        "a",
        "h",
        "h",
        "a",
    ],
}

matches_df_tw = pd.DataFrame(_df_data_tw).set_index(["id", "date number"])


_df_data_permutation = {
    "id": [
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "2",
        "2",
        "2",
        "2",
        "2",
        "2",
    ],
    "date number": [
        0,
        0,
        0,
        1,
        1,
        2,
        2,
        3,
        0,
        0,
        1,
        1,
        2,
        2,
    ],
    "home": [
        "a",
        "b",
        "a",
        "c",
        "d",
        "c",
        "a",
        "b",
        "one",
        "two",
        "two",
        "one",
        "three",
        "three",
    ],
    "away": [
        "d",
        "c",
        "b",
        "b",
        "b",
        "a",
        "d",
        "c",
        "three",
        "one",
        "three",
        "two",
        "two",
        "one",
    ],
    "winner": [
        "h",
        "d",
        "d",
        "a",
        "d",
        "a",
        "a",
        "h",
        "d",
        "d",
        "a",
        "h",
        "h",
        "a",
    ],
}

matches_df_permutations = pd.DataFrame(_df_data_permutation).set_index(
    ["id", "date number"]
)
