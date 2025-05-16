from typing import List, Tuple
from src.algorithms.heuristics import (
    Heuristic,
    IsolationHeuristic,
)
from src.algorithms.minmax import AlphaBetaMinmax, Minmax

from src.game.board import Board
from src.enums.color import Color
from src.game.move import Move


class Player:
    color: Color
    minmax: Minmax
    current_heuristic: Heuristic

    def __init__(
        self, color: Color, minmax: Minmax, heuristic: Heuristic | None = None
    ) -> None:
        if heuristic is None:
            heuristic = IsolationHeuristic()
        self.color = color
        self.minmax = minmax
        self.current_heuristic = heuristic

    def choose_move(self, board: Board) -> Move | None:
        if not self.minmax:
            return board.calculate_possible_moves(self.color)[0]
        return self.minmax.execute(board, self.color, self.current_heuristic)

    def __str__(self) -> str:
        return f"Player {self.color}"

    def __repr__(self) -> str:
        return f"Player(color={self.color}, minmax={self.minmax}, heuristic={self.current_heuristic})"

    def acknowledge_experiences(
        self,
        experiences: List[Tuple[Board, Color]],
        outcome: int,
    ) -> None:
        experiences = [
            (board, color, outcome)
            for board, color in experiences
            if color == self.color
        ]
        self.current_heuristic.apply_experiences(experiences)

    @staticmethod
    def create_default_players(
        minmax_cls=AlphaBetaMinmax,
        depth: int = 4,
        heuristic: Heuristic | None = None,
    ) -> Tuple["Player", "Player"]:
        if heuristic is None:
            heuristic = IsolationHeuristic

        white_player = Player(Color.WHITE, minmax_cls(depth), heuristic())
        black_player = Player(Color.BLACK, minmax_cls(depth), heuristic())
        return white_player, black_player
