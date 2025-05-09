import pytest
from src.enums.move_direction import MoveDirection
from src.enums.cell_state import CellState
from src.game.move import Move
from src.game.board import Board


def test_single_move():
    board = Board(8, 8)

    move_direction = MoveDirection.DOWN
    start_x, start_y = 3, 3
    start_cell = board.get_cell((start_x, start_y))
    for dx, dy in move_direction.all():
        board_copy = board.get_copy()
        end_x, end_y = start_x + dx, start_y + dy
        move = Move(0, start_x, start_y, end_x, end_y)
        captured_cell = board_copy.perform_move(move)
        end_cell = board_copy.get_cell((end_x, end_y))
        assert CellState(board_copy.get_cell((start_x, start_y))) == CellState.EMPTY
        assert end_cell == start_cell
        assert captured_cell != start_cell


def test_undo_move():
    board = Board(8, 8)
    board.print_board()
    start_x, start_y = 0, 0
    dx, dy = MoveDirection.DOWN.value
    end_x, end_y = start_x + dx, start_y + dy
    move = Move(0, start_x, start_y, end_x, end_y)
    captured_cell = board.perform_move(move)
    board.undo_move(move, captured_cell)
    assert CellState(board.get_cell((start_x, start_y))) == CellState.WHITE
    assert CellState(board.get_cell((end_x, end_y))) == CellState.BLACK
    assert CellState(captured_cell) == CellState.BLACK


def test_board_behavior():
    board = Board(8, 8)
    board.print_board()
    assert CellState(board.get_cell((0, 0))) == CellState.WHITE
    assert CellState(board.get_cell((1, 1))) == CellState.WHITE
    assert CellState(board.get_cell((0, 1))) == CellState.BLACK
    assert CellState(board.get_cell((1, 0))) == CellState.BLACK
    assert CellState(board.get_cell((7, 7))) == CellState.WHITE
    assert CellState(board.get_cell((7, 6))) == CellState.BLACK
    assert CellState(board.get_cell((-1, -1))) == CellState.EMPTY
    assert CellState(board.get_cell((8, 8))) == CellState.EMPTY
