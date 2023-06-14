from typing import Literal

from .circle_method import CircleMethod

MethodNames = Literal["circle"]
name_to_scheduling_func = {
    "circle": CircleMethod.generate_schedule,
}

__all__ = ["CircleMethod", "MethodNames", "name_to_scheduling_func"]
