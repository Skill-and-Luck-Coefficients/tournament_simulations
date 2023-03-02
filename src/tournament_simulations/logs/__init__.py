"""
    Provide loggers to different files.
"""

from . import logs
from .logging_decorator import log
from .logs import tournament_simulations_logger

__all__ = ["logs", "log", "tournament_simulations_logger"]
