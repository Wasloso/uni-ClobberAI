from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2

    def __str__(self):
        return "W" if self == Color.WHITE else "B"

    @staticmethod
    def from_char(char: str) -> "Color":
        return {"W": Color.WHITE, "B": Color.BLACK}[char]

    def __neg__(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE
