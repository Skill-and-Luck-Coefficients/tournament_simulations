"""
Simulations match-wide, that is, each matchhas its own probability:
[prob home win, prob draw, prob away win].
"""

from .batch import batch_simulate_points_per_match, batch_simulate_winners

__all__ = ["batch_simulate_points_per_match", "batch_simulate_winners"]
