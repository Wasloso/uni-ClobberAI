from typing import List, Tuple
from src.enums.color import Color
from src.utils.decorators import timeit
from .game_result import GameResult
from src.enums.game_state import GameState
from src.player.player import Player
from src.game.board import Board


class Game:
    board: Board
    state: GameState = GameState.WAITING
    history = List[Tuple[Board, Color]]

    def __init__(self, n: int = 10, m: int = 10):
        self.board = Board(n, m)
        self.history = []

    def play_one_turn(self, player: Player) -> GameState:
        move = player.choose_move(self.board)
        if not move:
            return GameState.FINISHED
        print(
            f"{player} moves from ({move.x_start},{move.y_start}) to ({move.x_end},{move.y_end}), move score: {move.score}"
        )
        self.board.perform_move(move)
        self.board.print_board()
        return GameState.IN_PROGRESS

    @timeit
    def play(self, player_one: Player, player_two: Player) -> GameResult:
        self.history = []
        current_player: Player = player_one
        while self.state != GameState.FINISHED:
            self.history.append((self.board.get_copy(), current_player.color))
            self.state = self.play_one_turn(current_player)
            current_player = player_one if current_player == player_two else player_two
        winner: Player = current_player
        loser: Player = player_one if current_player == player_two else player_two

        result: GameResult = GameResult(winner, *self.board.calculate_state())
        winner.acknowledge_experiences(self.history, 1)
        loser.acknowledge_experiences(self.history, -1)

        print(result)
        return result

    @timeit
    def play_tournament(
        self, player_one: Player, player_two: Player, rounds: int = 5
    ) -> None:
        points = {player_one: 0, player_two: 0}
        for i in range(rounds):
            print(f"Round {i + 1} of {rounds}")
            result: GameResult = self.play(player_one, player_two)
            points[result.winner] += 1
            self.board.reset()
            self.history.clear()
            self.state = GameState.WAITING
        print("Tournament results:")
        for player, score in points.items():
            print(f"{player}: {score} points")
