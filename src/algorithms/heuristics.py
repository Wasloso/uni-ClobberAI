from abc import ABC, abstractmethod
from src.enums.move_direction import MoveDirection
from src.game.board import Board
from src.enums.color import Color
from src.utils.decorators import timeit


class Heuristic(ABC):
    def __init__(self):
        self._cache = {}

    @abstractmethod
    def _evaluate(self, board: Board, color: Color) -> float:
        pass

    def evaluate(self, board: Board, color: Color) -> float:
        key = (hash(board), color)
        if key not in self._cache:
            self._cache[key] = self._evaluate(board, color)
        return self._cache[key]

    def clear_cache(self):
        self._cache.clear()


class MobilityHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        return len(board.calculate_possible_moves(color)) - len(
            board.calculate_possible_moves(-color)
        )


@timeit(precision=6)
class CountHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        return board.pieces_count(color) - board.pieces_count(-color)


@timeit(precision=8)
class IsolationHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        player_score = self._calculate_score(board, color)
        opponent_score = self._calculate_score(board, -color)
        return player_score - opponent_score

    def _calculate_score(self, board: Board, color: Color) -> int:
        cells = board.get_cells_with_color(color)
        total = len(cells)
        isolated = sum(1 for x, y in cells if board.is_isolated(x, y))
        return total - isolated


class AdaptiveHeuristic(Heuristic):
    def __init__(self):
        super().__init__()
        self.count: Heuristic = CountHeuristic()
        self.mobility: Heuristic = MobilityHeuristic()
        self.isolation: Heuristic = IsolationHeuristic()
        self.active_heuristic: Heuristic = self.mobility  # default

    def _evaluate(self, board: Board, color: Color) -> float:
        progress = board.occupied_cells() / board.total_cells()
        # TODO: Make this more dynamic and adaptive
        if progress < 0.3:
            return self.mobility.evaluate(board, color)
        elif progress < 0.7:
            return self.isolation.evaluate(board, color)
        else:
            return self.count.evaluate(board, color)


if __name__ == "__main__":
    board = Board(5, 5)
    heuristic = IsolationHeuristic()
    player_color = Color.WHITE
    enemy_color = Color.BLACK
    value_player = heuristic.evaluate(board, player_color)
    value_enemy = heuristic.evaluate(board, enemy_color)
    print(f"Player: {value_player}, Enemy: {value_enemy}")
