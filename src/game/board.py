import numpy as np
from typing import Dict, List, Tuple
from src.enums.color import Color
from src.enums.move_direction import MoveDirection
from src.enums.cell_state import CellState
from .move import Move


class Board:
    _board: np.ndarray
    _n: int
    _m: int

    def __init__(self, n: int = 10, m: int = 10):
        self._n = n
        self._m = m
        self._board = self._create_board(n, m)

    def _create_board(self, n: int, m: int) -> np.ndarray:
        board = np.empty((n, m), dtype=np.uint8)
        for row in range(n):
            for col in range(m):
                state = CellState.WHITE if (row + col) % 2 == 0 else CellState.BLACK
                board[row, col] = state.value
        return board

    def print_board(self) -> None:
        print(
            "\n".join(
                " ".join(str(CellState(cell)) for cell in row) for row in self._board
            )
        )

    def get_cell(self, position: Tuple[int, int]) -> CellState:
        x, y = position
        if not self.is_within_bounds(x, y):
            return CellState.EMPTY
        return CellState(self._board[y, x])

    def set_cell(self, position: Tuple[int, int], state: CellState) -> None:
        x, y = position
        self._board[y, x] = state.value

    def get_copy(self) -> "Board":
        new_board = Board(self._n, self._m)
        new_board._board = np.copy(self._board)
        return new_board

    def perform_move(self, move: Move) -> CellState:
        start_x, start_y = move.x_start, move.y_start
        end_x, end_y = move.x_end, move.y_end

        start_cell: CellState = self.get_cell((start_x, start_y))
        caputred_cell: CellState = self.get_cell((end_x, end_y))
        if caputred_cell == CellState.EMPTY or start_cell == caputred_cell:
            return None
        self.set_cell((end_x, end_y), start_cell)
        self.set_cell((start_x, start_y), CellState.EMPTY)
        return caputred_cell

    def undo_move(self, move: Move, captured_cell: CellState) -> None:
        start_x, start_y = move.x_start, move.y_start
        end_x, end_y = move.x_end, move.y_end
        end_cell: CellState = self.get_cell((end_x, end_y))

        self.set_cell((start_x, start_y), end_cell)
        self.set_cell((end_x, end_y), captured_cell)

    def get_cells_with_color(self, color: Color) -> List[Tuple[int, int]]:
        return list(zip(*np.where(self._board == color.value)))

    def to_dict(self) -> Dict[Tuple[int, int], CellState]:
        return {
            (x, y): CellState(self._board[x, y])
            for x in range(self._n)
            for y in range(self._m)
        }

    def get_all_cells(self) -> List[Tuple[int, int]]:
        return [
            (i, j)
            for i in range(self._board.shape[0])
            for j in range(self._board.shape[1])
        ]

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._m and 0 <= y < self._n

    def calculate_state(self) -> Tuple[int, int, str]:
        white_points: int = np.count_nonzero(self._board == Color.WHITE.value)
        black_points: int = np.count_nonzero(self._board == Color.BLACK.value)

        winner = (
            Color.WHITE
            if white_points > black_points
            else Color.BLACK if black_points > white_points else "Draw"
        )
        return winner, white_points, black_points

    def evaluate_for_color(self, color: Color) -> int:
        return np.sum(self._board == color.value) - np.sum(self._board == -color.value)

    def calculate_possible_moves(self, color: Color) -> List[Move]:
        enemy_color: Color = -color
        player_cells: List[Tuple[int, int]] = self.get_cells_with_color(color)
        possible_moves: List[Move] = []

        for start_y, start_x in player_cells:
            for direction in MoveDirection:
                dx, dy = direction.value
                end_x, end_y = start_x + dx, start_y + dy
                end_cell: CellState = self.get_cell((end_x, end_y))

                if end_cell == CellState.EMPTY:
                    continue
                if end_cell.to_color() == enemy_color:
                    possible_moves.append(Move(0, start_x, start_y, end_x, end_y))
        return possible_moves

    def is_valid_move(self, move: Move, color: Color):
        end_cell_color: Color = self.get_cell((move.x_end, move.y_end)).to_color()
        if not end_cell_color:
            return False
        if color == -end_cell_color:
            return True

    def is_isolated(self, x: int, y: int):
        color: Color = self.get_cell((x, y)).to_color()
        if not color:
            raise ValueError("This cell is empty, it cannot be isolated")
        for dx, dy in MoveDirection.all():
            move: Move = Move(0, x, y, x + dx, y + dy)
            if self.is_valid_move(move, color):
                return False
        return True

    def total_cells(self) -> int:
        return len(self)

    def occupied_cells(self) -> int:
        return np.count_nonzero(self._board != CellState.EMPTY.value)

    def pieces_count(self, color: Color) -> int:
        return np.count_nonzero(self._board == color.value)

    def get_hash(self) -> int:
        return hash(self._board.tobytes())

    def __len__(self) -> int:
        return self._n * self._m


if __name__ == "__main__":
    board = Board(8, 8)

    board.calculate_possible_moves(Color.WHITE)
    print(len(board))
