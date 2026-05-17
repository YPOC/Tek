import random
import logging
from src.Player import Player
from src.PlayerStrategy import RandomStrategy, ScaredyStrategy
from src.Game import Game

logging.basicConfig(level=logging.INFO)

random.seed(123)
players = [
    Player("Kim", ScaredyStrategy),
    Player("Rachid", RandomStrategy),
    Player("Moha", RandomStrategy),
    Player("Yannick", RandomStrategy)
]
game = Game(players)
game.play_game(n_rounds = 1000)