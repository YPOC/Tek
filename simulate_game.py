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

# Issues
# 1. After a Jack has been played and a suit has been wished, the wish gets ignored
# 2. When a Joker has been played, the following legal cards are only Jacks (or maybe Jokers?)
# 3. When chaining, the 2nd card is processed correctly but for the third one the player_index stays at the same player as before. This also needs to advance the player index
# 4. When a player draws a card, they only get the chance to play that exact card
# 5. When a player can't draw a card due to an empty draw stack, their n_turns_to_skip gets increased but it should also be decreased right after
# 6. There's no check if a player needs to skip a turn
# 7. There's no check if the draw stack is empty and all players can't play