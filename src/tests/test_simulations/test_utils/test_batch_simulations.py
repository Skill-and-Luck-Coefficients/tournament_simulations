from typing import Callable

import pandas as pd
import pytest

import simulations.utils.batch_simulations as bat


@pytest.fixture
def simul_func():
    def simulation_func(num_simulations):
        dfs = [pd.DataFrame({"ok": [0, 1, 2]})] * num_simulations
        return pd.concat(dfs, ignore_index=True)

    return simulation_func


@pytest.fixture
def first_after_func():
    def after_func(df):
        return df + 2

    return after_func


@pytest.fixture
def second_after_func():
    def after_func(df):
        return df.set_axis(["col"], axis="columns")

    return after_func


def test_batch_simulate_tournaments_first(simul_func: Callable):

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=1,
        num_simul_per_iteration=1,
        func_after_simulation=lambda x: x,
    )
    data = [[0], [1], [2]]
    expected = pd.DataFrame(data=data, columns=["ok"] * 1)
    assert simulated.equals(expected)

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=3,
        num_simul_per_iteration=1,
        func_after_simulation=lambda x: x,
    )
    data = [[0] * 3, [1] * 3, [2] * 3]
    expected = pd.DataFrame(data=data, columns=["ok"] * 3)
    assert simulated.equals(expected)

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=1,
        num_simul_per_iteration=3,
        func_after_simulation=lambda x: x,
    )
    data = [[0], [1], [2]] * 3
    expected = pd.DataFrame(data=data, columns=["ok"] * 1)
    assert simulated.equals(expected)

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=2,
        num_simul_per_iteration=3,
        func_after_simulation=lambda x: x,
    )
    data = [[0] * 2, [1] * 2, [2] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["ok"] * 2)
    assert simulated.equals(expected)


def test_batch_simulate_tournaments_second(
    simul_func: Callable, first_after_func: Callable
):

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=1,
        num_simul_per_iteration=1,
        func_after_simulation=first_after_func,
    )
    data = [[2], [3], [4]]
    expected = pd.DataFrame(data=data, columns=["ok"] * 1)
    assert simulated.equals(expected)

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=2,
        num_simul_per_iteration=3,
        func_after_simulation=first_after_func,
    )
    data = [[2] * 2, [3] * 2, [4] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["ok"] * 2)
    assert simulated.equals(expected)


def test_batch_simulate_tournaments_third(
    simul_func: Callable, second_after_func: Callable
):

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=4,
        num_simul_per_iteration=1,
        func_after_simulation=second_after_func,
    )
    data = [[0] * 4, [1] * 4, [2] * 4]
    expected = pd.DataFrame(data=data, columns=["col"] * 4)
    assert simulated.equals(expected)

    simulated = bat._batch_simulate_tournaments(
        simul_func,
        num_iterations=2,
        num_simul_per_iteration=3,
        func_after_simulation=second_after_func,
    )
    data = [[0] * 2, [1] * 2, [2] * 2] * 3
    expected = pd.DataFrame(data=data, columns=["col"] * 2)
    assert simulated.equals(expected)


def test_create_column_names():

    assert bat._create_column_names(0) == []
    assert bat._create_column_names(1) == ["s0"]
    assert bat._create_column_names(3) == ["s0", "s1", "s2"]
    assert bat._create_column_names(6) == ["s0", "s1", "s2", "s3", "s4", "s5"]


def test_batch_simulate_tournaments_template(
    simul_func: Callable, first_after_func: Callable
):

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iteration_simulation=(4, 1),
        func_after_simulation=first_after_func,
    )
    data = [[2] * 4, [3] * 4, [4] * 4]
    expected = pd.DataFrame(data=data, columns=["s0", "s1", "s2", "s3"])
    assert simulated.equals(expected)

    simulated = bat.batch_simulate_tournaments_template(
        simul_func,
        num_iteration_simulation=(2, 1),
        func_after_simulation=first_after_func,
    )
    data = [[2] * 2, [3] * 2, [4] * 2]
    expected = pd.DataFrame(data=data, columns=["s0", "s1"])
    assert simulated.equals(expected)
