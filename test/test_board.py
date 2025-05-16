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


def test_board_hash():
    board = Board(8, 8)  # Initialize a board
    hash1 = board.get_hash()
    move = Move(
        x_start=0,
        y_start=0,
        x_end=0,
        y_end=1,
        score=0,
    )
    captured = board.perform_move(move)
    board.undo_move(move, captured)
    hash2 = board.get_hash()
    assert hash1 == hash2, "Board hash changed after perform/undo move!"
    print(f"Hash consistency check passed: {hash1}")
