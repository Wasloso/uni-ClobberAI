from src.player.player import Player
from src.game.game import Game

if __name__ == "__main__":

    game: Game = Game(8, 8)
    player_white, player_black = Player.create_default_players()
    game.play(player_white, player_black)
