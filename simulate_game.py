import random
import logging
from src.Player import Player
from src.PlayerStrategy import RandomStrategy
from src.Game import Game

logging.basicConfig(level=logging.DEBUG)

random.seed(123)
players = [Player("Kim", RandomStrategy), Player("Rachid", RandomStrategy), Player("Moha", RandomStrategy), Player("Yannick", RandomStrategy)]
game = Game(players)
game.play_game(n_rounds = 4)