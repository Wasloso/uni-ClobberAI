from typing import List
from src.utils.decorators import timeit
from .game_result import GameResult
from src.enums.game_state import GameState
from src.player.player import Player
from src.game.board import Board


class Game:
    board: Board
    players: List[Player]
    state: GameState = GameState.WAITING

    def __init__(self, n: int = 10, m: int = 10):
        self.board = Board(n, m)
        self.game_over = False
        self.winner = None

    def play_one_turn(self, player: Player) -> GameState:
        move = player.choose_move(self.board)
        if not move:
            return GameState.FINISHED
        print(
            f"{player} moves from ({move.x_start},{move.y_start}) to ({move.x_end},{move.y_end})"
        )
        self.board.perform_move(move)
        self.board.print_board()
        return GameState.IN_PROGRESS

    @timeit
    def play(self, player_one: Player, player_two: Player) -> None:
        current_player: Player = player_one
        while self.state != GameState.FINISHED:
            self.state = self.play_one_turn(current_player)
            current_player = player_one if current_player == player_two else player_two
        result: GameResult = GameResult(*self.board.calculate_state())
        print(result)
