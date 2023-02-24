import pandas as pd

_df_data_mw = {
    "id": [
        "T/1",
        "T/1",
        "T/1",
        "T/1",
        "T/1",
        "T/1",
        "T/2",
        "T/2",
        "T/2",
        "T/2",
        "T/2",
        "T/2",
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
        "away",
        "home",
        "away",
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
        "home",
        "away",
        "home",
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
    "probabilities": [
        (1, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, 1),
        (0, 0, 1),
        (1, 0, 0),
        (0.333, 0.333, 0.334),
        (0.333, 0.333, 0.334),
        (0.333, 0.333, 0.334),
        (0.333, 0.333, 0.334),
        (0.333, 0.333, 0.334),
        (0.333, 0.333, 0.334),
    ],
}

matches_df_mw = (
    pd.DataFrame(_df_data_mw)
    .astype({"id": "category"})
    .set_index(["id", "date number"])
)

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

matches_df_tw = (
    pd.DataFrame(_df_data_tw)
    .astype({"id": "category"})
    .set_index(["id", "date number"])
)
