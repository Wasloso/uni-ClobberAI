import pytest

from src.enums.color import Color
from src.algorithms import IsolationHeuristic
from src.enums.move_direction import MoveDirection
from src.enums.cell_state import CellState
from src.game.move import Move
from src.game.board import Board


def test_isolation_heuristic_both_zero():
    board: Board = Board(5, 5)
    heuristic: IsolationHeuristic = IsolationHeuristic()
    player_color: Color = Color.WHITE
    enemy_color: Color = Color.BLACK
    value_player = heuristic.evaluate(board, player_color)
    value_enemy = heuristic.evaluate(board, enemy_color)
    assert value_player == 1
    assert value_enemy == -1


def test_isolation_one_isolated():
    board: Board = Board(5, 5)
    heuristic: IsolationHeuristic = IsolationHeuristic()
    board.set_cell((0, 1), CellState.EMPTY)
    board.set_cell((1, 1), CellState.EMPTY)
    board.set_cell((1, 0), CellState.EMPTY)
    player_color: Color = Color.WHITE
    board.print_board()
    value_player = heuristic.evaluate(board, player_color)
    assert value_player == 1
