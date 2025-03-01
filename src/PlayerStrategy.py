from abc import ABC, abstractmethod
from collections import namedtuple
import random
from .Card import Card, Suit

class PlayerStrategy(ABC):
    @staticmethod
    @abstractmethod
    def play(hand: list[Card], top_card: Card, legal_moves: list[Card]) -> Card:
        raise NotImplementedError("Subclasses need to implement this!")


    @staticmethod
    @abstractmethod
    def choose_suit(*args) -> Suit:
        raise NotImplementedError("Subclasses need to implement this!")



class RandomStrategy(PlayerStrategy):
    # play a random card
    @staticmethod
    def play(hand: list[Card], top_card: Card, legal_moves: list[Card]) -> Card:
        return random.choice(legal_moves) if legal_moves else None


    @staticmethod
    def choose_suit(*args):
        return random.choice([suit for suit in Suit if suit is not Suit.JOKER])



class ScaredyStrategy(PlayerStrategy):
    @staticmethod
    def play(hand: list[Card], top_card: Card, legal_moves: list[Card]) -> Card:
        # play the card worth most points
        return sorted(legal_moves, key=lambda card: card.value, reverse=True)[0]


    @staticmethod
    def choose_suit(hand: list[Card], top_card: Card) -> Suit:
        # choose the suit where the player has the most points of in hand
        SuitValues = namedtuple("SuitValues", ["value", "suit"])
        return sorted(
            [
                SuitValues(
                    sum([card.value for card in hand if card.suit is suit]),
                    suit
                ) for suit in Suit if suit is not Suit.JOKER
            ],
            key = lambda suit_values: suit_values.value,
            reverse = True
        )[0].suit