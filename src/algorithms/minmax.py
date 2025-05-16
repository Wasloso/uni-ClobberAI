from abc import ABC, abstractmethod
import random
from typing import Tuple

from src.enums.color import Color
from src.game.board import Board
from src.game.move import Move
from src.utils.decorators import timeit
from .heuristics import Heuristic


class Minmax(ABC):
    def __init__(self, depth: int = 2):
        self.depth = depth
        self.transposition_table = {}

    @abstractmethod
    def execute(
        self, board: Board, player_color: Color, heuristic: Heuristic | None = None
    ) -> Move | None:
        raise NotImplementedError("Subclasses should implement this method.")

    def _minmax(
        self,
        board: Board,
        depth: int,
        maximizing: bool,
        color: Color,
        self_color: Color,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
        use_pruning: bool = False,
        heuristic: Heuristic | None = None,
    ) -> Tuple[float, Move | None]:
        board_hash = (board.get_hash(), color.value, maximizing)

        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        if depth == 0:
            value = heuristic.evaluate(board, self_color)
            self.transposition_table[board_hash] = (value, None)
            return value, None
        moves = board.calculate_possible_moves(color)
        if not moves:
            return float("-inf") if maximizing else float("+inf"), None

        best_move: Move = None
        best_eval = float("-inf") if maximizing else float("inf")

        for move in moves:
            captured = board.perform_move(move)

            eval_score, _ = self._minmax(
                board,
                depth - 1,
                not maximizing,
                -color,
                self_color,
                alpha,
                beta,
                use_pruning,
                heuristic,
            )

            board.undo_move(move, captured)
            move.score = eval_score

            if (maximizing and eval_score >= best_eval) or (
                not maximizing and eval_score <= best_eval
            ):
                best_eval = eval_score
                best_move = move

            if use_pruning:
                if maximizing:
                    alpha = max(alpha, eval_score)
                else:
                    beta = min(beta, eval_score)
                if beta <= alpha:
                    break

        self.transposition_table[board_hash] = (best_eval, best_move)
        return best_eval, best_move


class BaseMinmax(Minmax):
    def execute(
        self, board: Board, color: Color, heuristic: Heuristic | None = None
    ) -> Move | None:
        heuristic = heuristic
        self.transposition_table.clear()
        _, move = self._minmax(
            board, self.depth, True, color, color, heuristic=heuristic
        )
        return move


class AlphaBetaMinmax(Minmax):
    def execute(
        self, board: Board, color: Color, heuristic: Heuristic | None = None
    ) -> Move | None:
        heuristic = heuristic
        self.transposition_table.clear()
        _, move = self._minmax(
            board, self.depth, True, color, color, use_pruning=True, heuristic=heuristic
        )
        return move
