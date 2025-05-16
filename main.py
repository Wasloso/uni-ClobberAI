from src.algorithms.minmax import BaseMinmax
from src.algorithms.heuristics import (
    ConnectivityHeuristic,
    ControlHeuristic,
    EdgePositionHeuristic,
    IsolationHeuristic,
    RLHeuristic,
    RandomHeuristic,
)
from src.player.player import Player
from src.game.game import Game

if __name__ == "__main__":

    game: Game = Game(5, 5)
    player_white, player_black = Player.create_default_players(depth=3)
    player_white.current_heuristic = RLHeuristic(
        heuristics=[
            ConnectivityHeuristic,
            IsolationHeuristic,
            ControlHeuristic,
        ]
    )
    game.play_tournament(
        player_white,
        player_black,
        100,
    )
