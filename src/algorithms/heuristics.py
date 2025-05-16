from abc import ABC, abstractmethod
import random
from typing import List, Tuple
from src.enums.move_direction import MoveDirection
from src.game.board import Board
from src.enums.color import Color
from src.utils.decorators import timeit
from math import tanh


class Heuristic(ABC):
    def __init__(self):
        self._cache = {}

    @abstractmethod
    def _evaluate(self, board: Board, color: Color) -> float:
        pass

    def evaluate(self, board: Board, color: Color) -> float:

        # key = (board.get_hash(), color.value)

        # if key in self._cache:
        #     return self._cache[key]
        value = self._evaluate(board, color)

        # self._cache[key] = value

        return value

    def clear_cache(self):
        print("Clearing cache")
        self._cache.clear()

    def apply_experiences(self, experiences: List[Tuple[Board, Color, float]]) -> None:
        pass


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


class ControlHeuristic(Heuristic):
    def _evaluate(self, board, color):
        player_score = self._calculate_score(board, color)
        opponent_score = self._calculate_score(board, -color)
        return player_score - opponent_score

    def _calculate_score(self, board: Board, color: Color) -> float:
        cells: List[Tuple[int, int]] = board.get_cells_with_color(color)
        score = sum(
            map(lambda cell: self._calculate_distance_score(board, cell), cells)
        )
        return score

    def _calculate_distance_score(
        self, board: Board, position: Tuple[int, int]
    ) -> float:
        x, y = position
        cx, cy = board.center
        return 1 / (1 + (x - cx) ** 2 + (y - cy) ** 2)


class ConnectivityHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        player_score = self._calculate_connectivity(board, color)
        opponent_score = self._calculate_connectivity(board, -color)
        return player_score - opponent_score

    def _calculate_connectivity(self, board: Board, color: Color) -> int:
        cells = board.get_cells_with_color(color)
        visited = set()
        total = 0

        for x, y in cells:
            if (x, y) not in visited:
                group_size = self._flood_fill(board, x, y, color, visited)
                total += group_size * group_size
        return total

    def _flood_fill(
        self, board: Board, x: int, y: int, color: Color, visited: set
    ) -> int:
        stack = [(x, y)]
        count = 0

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited or not board.is_within_bounds(cx, cy):
                continue

            if board.get_cell((cx, cy)).to_color() == color:
                visited.add((cx, cy))
                count += 1
                for dx, dy in MoveDirection.all():
                    stack.append((cx + dx, cy + dy))
        return count


class EdgePositionHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        player_penalty = self._calculate_penalty(board, color)
        opponent_penalty = self._calculate_penalty(board, -color)
        return opponent_penalty - player_penalty

    def _calculate_penalty(self, board: Board, color: Color) -> float:
        cells: List[Tuple[int, int]] = board.get_cells_with_color(color)
        penalty = 0
        n, m = board._n, board._m

        for x, y in cells:
            is_corner = (x == 0 or x == m - 1) and (y == 0 or y == n - 1)
            is_edge = x == 0 or x == m - 1 or y == 0 or y == n - 1
            if is_corner:
                penalty += 2
            elif is_edge:
                penalty += 1
        return penalty


class WeightedHeuristic(Heuristic):
    def __init__(self, heuristics: List[Tuple[Heuristic, float]]):
        super().__init__()
        self._heuristics: List[Tuple[Heuristic, float]] = []
        for heuristicCls, weight in heuristics:
            self._heuristics.append((heuristicCls(), weight))

    def _evaluate(self, board: Board, color: Color) -> float:
        total_score = 0
        for heuristic_instance, weight in self._heuristics:
            total_score += heuristic_instance.evaluate(board, color) * weight
        return total_score

    def clear_cache(self):
        super().clear_cache()
        for heuristic_instance, _ in self._heuristics:
            heuristic_instance.clear_cache()

    @staticmethod
    def create_default_heuristic() -> "WeightedHeuristic":
        heuristics = [
            (IsolationHeuristic, 0.5),
            (ControlHeuristic, 0.3),
            (ConnectivityHeuristic, 0.7),
            (EdgePositionHeuristic, 0.2),
        ]
        return WeightedHeuristic(heuristics)


class RandomHeuristic(Heuristic):
    def _evaluate(self, board: Board, color: Color) -> float:
        return random.uniform(-100, 100)


class RLHeuristic(Heuristic):
    def __init__(
        self, heuristics: List[Heuristic], initial_weights: List[float] | None = None
    ):
        super().__init__()
        self._heuristic_instances: List[Heuristic] = [H() for H in heuristics]

        if initial_weights is None:
            self._weights = [1.0] * len(heuristics)
        else:
            self._weights = list(initial_weights)

    def _evaluate(self, board: Board, color: Color) -> float:
        total_score = 0.0
        for i, heuristic_instance in enumerate(self._heuristic_instances):
            feature_value = tanh(heuristic_instance.evaluate(board, color))
            total_score += feature_value * self._weights[i]

        return total_score

    def apply_experiences(self, experiences: List[Tuple[Board, Color, float]]):
        self.update_weights(experiences)

    def update_weights(
        self, experiences: List[Tuple[Board, Color, float]], learning_rate: float = 0.01
    ):

        if not experiences:
            return
        self.clear_cache()
        for h_instance in self._heuristic_instances:
            h_instance.clear_cache()

        for board_state, color, final_outcome in experiences:
            predicted_outcome = self._evaluate(board_state, color)
            error = final_outcome - predicted_outcome
            for i, heuristic_instance in enumerate(self._heuristic_instances):
                feature_value = tanh(heuristic_instance._evaluate(board_state, color))
                self._weights[i] += learning_rate * error * feature_value
        print("Updated weights:", self._weights)
