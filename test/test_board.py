import pytest

from src.enums.move_direction import MoveDirection
from src.enums.cell_state import CellState
from src.game.move import Move
from src.game.board import Board


def test_isolation_all():
    board: Board = Board(3, 3)
    board.print_board()
    cells = board.get_all_cells()

    for y, x in cells:
        isolated = board.is_isolated(x, y)
        assert not isolated
