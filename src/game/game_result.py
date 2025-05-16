from dataclasses import dataclass

from src.player.player import Player


@dataclass
class GameResult:
    winner: Player
    white_points: int
    black_points: int

    def __str__(self):
        return f"Winner: {self.winner}, White pieces left: {self.white_points}, Black pieces left: {self.black_points}"
