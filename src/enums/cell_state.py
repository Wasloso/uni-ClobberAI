from enum import Enum
from .color import Color


class CellState(Enum):
    EMPTY = 0
    WHITE = Color.WHITE.value
    BLACK = Color.BLACK.value

    def __str__(self):
        if self == CellState.EMPTY:
            return "_"
        return str(Color(self.value))

    @staticmethod
    def from_char(char: str) -> "CellState":
        if char == "_":
            return CellState.EMPTY
        return CellState(Color.from_char(char).value)

    def to_color(self) -> Color | None:
        if self in {CellState.WHITE, CellState.BLACK}:
            return Color(self.value)
        return None
