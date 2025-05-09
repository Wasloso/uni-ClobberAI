from dataclasses import dataclass


@dataclass
class Move:
    score: int
    x_start: int
    y_start: int
    x_end: int
    y_end: int
