from typing import TypeVar

Team = TypeVar("Team")
Match = tuple[Team, Team]  # each team is an integer
Round = tuple[Match, ...]
