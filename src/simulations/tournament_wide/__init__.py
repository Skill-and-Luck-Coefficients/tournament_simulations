"""
Simulations tournament-wide, that is, each tournament has its own probability:
[prob home win, prob draw, prob away win]. All matches for a tournament
will have the same probability
"""

from .batch import batch_simulate_points_per_match, batch_simulate_winners

__all__ = ["batch_simulate_points_per_match", "batch_simulate_winners"]
