from enum import Enum
from typing import List, Tuple


class MoveDirection(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def all(cls) -> List[Tuple[int, int]]:
        return [d.value for d in cls]
