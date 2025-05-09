from typing import Dict, List, Tuple, Optional
from src.enums.color import Color
from src.enums.move_direction import MoveDirection
from src.enums.cell_state import CellState
from .move import Move


class Board:
    _board: List[List[int]]
    _n: int
    _m: int

    def __init__(self, n: int = 10, m: int = 10):
        self._n = n
        self._m = m
        self._board = self._create_board(n, m)

    def _create_board(self, n: int, m: int) -> List[List[int]]:
        board = []
        for y in range(n):  # rows
            row = []
            for x in range(m):  # columns
                state = CellState.WHITE if (x + y) % 2 == 0 else CellState.BLACK
                row.append(state.value)
            board.append(row)
        return board

    def print_board(self) -> None:
        for row in self._board:
            print(" ".join(str(CellState(cell)) for cell in row))

    def get_cell(self, position: Tuple[int, int]) -> CellState:
        x, y = position
        if not self.is_within_bounds(x, y):
            return CellState.EMPTY
        return CellState(self._board[y][x])

    def set_cell(self, position: Tuple[int, int], state: CellState) -> None:
        x, y = position
        if state is None:
            state = CellState.EMPTY
        self._board[y][x] = state.value

    def get_copy(self) -> "Board":
        new_board = Board(self._n, self._m)
        new_board._board = [row[:] for row in self._board]
        return new_board

    def perform_move(self, move: Move) -> Optional[CellState]:
        start_x, start_y = move.x_start, move.y_start
        end_x, end_y = move.x_end, move.y_end

        start_cell = self.get_cell((start_x, start_y))
        captured_cell = self.get_cell((end_x, end_y))

        if captured_cell == CellState.EMPTY or start_cell == captured_cell:
            return None

        self.set_cell((end_x, end_y), start_cell)
        self.set_cell((start_x, start_y), CellState.EMPTY)
        return captured_cell

    def undo_move(self, move: Move, captured_cell: Optional[CellState]) -> None:
        start_x, start_y = move.x_start, move.y_start
        end_x, end_y = move.x_end, move.y_end
        end_cell = self.get_cell((end_x, end_y))

        self.set_cell((start_x, start_y), end_cell)
        self.set_cell(
            (end_x, end_y),
            captured_cell if captured_cell is not None else CellState.EMPTY,
        )

    def get_cells_with_color(self, color: Color) -> List[Tuple[int, int]]:
        cells = []
        for y in range(self._n):
            for x in range(self._m):
                if self._board[y][x] == color.value:
                    cells.append((x, y))
        return cells

    def to_dict(self) -> Dict[Tuple[int, int], CellState]:
        return {
            (x, y): CellState(self._board[y][x])
            for y in range(self._n)
            for x in range(self._m)
        }

    def get_all_cells(self) -> List[Tuple[int, int]]:
        return [(x, y) for y in range(self._n) for x in range(self._m)]

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._m and 0 <= y < self._n

    def calculate_state(self) -> Tuple[int, int, str]:
        white_points = sum(row.count(Color.WHITE.value) for row in self._board)
        black_points = sum(row.count(Color.BLACK.value) for row in self._board)

        winner = (
            Color.WHITE
            if white_points > black_points
            else Color.BLACK if black_points > white_points else "Draw"
        )
        return winner, white_points, black_points

    def evaluate_for_color(self, color: Color) -> int:
        color_count = sum(row.count(color.value) for row in self._board)
        enemy_count = sum(row.count(-color.value) for row in self._board)
        return color_count - enemy_count

    def calculate_possible_moves(self, color: Color) -> List[Move]:
        enemy_color = -color
        player_cells = self.get_cells_with_color(color)
        possible_moves = []

        for x, y in player_cells:
            for direction in MoveDirection:
                dx, dy = direction.value
                new_x, new_y = x + dx, y + dy

                if not self.is_within_bounds(new_x, new_y):
                    continue

                end_cell = self.get_cell((new_x, new_y))
                if end_cell.to_color() == enemy_color:
                    possible_moves.append(Move(0, x, y, new_x, new_y))
        return possible_moves

    def is_valid_move(self, move: Move, color: Color) -> bool:
        if not self.is_within_bounds(move.x_end, move.y_end):
            return False
        end_cell_color = self.get_cell((move.x_end, move.y_end)).to_color()
        return end_cell_color == -color

    def is_isolated(self, x: int, y: int) -> bool:
        color = self.get_cell((x, y)).to_color()
        if not color:
            raise ValueError("This cell is empty, it cannot be isolated")

        for dx, dy in MoveDirection.all():
            new_x, new_y = x + dx, y + dy
            if not self.is_within_bounds(new_x, new_y):
                continue

            if self.get_cell((new_x, new_y)).to_color() == -color:
                return False
        return True

    def total_cells(self) -> int:
        return len(self)

    def occupied_cells(self) -> int:
        return sum(
            1 for row in self._board for cell in row if cell != CellState.EMPTY.value
        )

    def pieces_count(self, color: Color) -> int:
        return sum(row.count(color.value) for row in self._board)

    def get_hash(self) -> int:
        return hash(tuple(tuple(row) for row in self._board))

    def __len__(self) -> int:
        return self._n * self._m
