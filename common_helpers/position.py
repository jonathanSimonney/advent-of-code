from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Class for position on an 2 dimensions board."""
    x: int
    y: int
