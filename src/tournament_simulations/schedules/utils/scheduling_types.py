from typing import TypeVar

Team = TypeVar("Team")
Match = tuple[Team, Team]
Round = tuple[Match, ...]
