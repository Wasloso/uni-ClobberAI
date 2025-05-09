from typing import List, Tuple
from src.algorithms.heuristics import Heuristic, MobilityHeuristic
from src.algorithms.minmax import AlphaBetaMinmax, Minmax

from src.game.board import Board
from src.enums.color import Color
from src.game.move import Move


class Player:
    color: Color
    minmax: Minmax
    current_heuristic: Heuristic

    def __init__(
        self, color: Color, minmax: Minmax, heuristic: Heuristic = MobilityHeuristic()
    ) -> None:
        self.color = color
        self.minmax = minmax
        self.current_heuristic = heuristic

    def choose_move(self, board: Board) -> Move | None:
        if not self.minmax:
            return board.calculate_possible_moves(self.color)[0]
        return self.minmax.execute(board, self.color, self.current_heuristic)

    def __str__(self) -> str:
        return f"Player {self.color}"

    @staticmethod
    def create_default_players(
        minmax_cls=AlphaBetaMinmax,
        depth: int = 4,
        heuristic: Heuristic = MobilityHeuristic(),
    ) -> Tuple["Player", "Player"]:

        white_player = Player(Color.WHITE, minmax_cls(depth), heuristic)
        black_player = Player(Color.BLACK, minmax_cls(depth), heuristic)
        return white_player, black_player
