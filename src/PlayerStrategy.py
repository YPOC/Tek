from abc import ABC, abstractmethod
import random
from typing import NamedTuple

from .Card import Card, Suit

class PlayerStrategy(ABC):
    @staticmethod
    @abstractmethod
    def play(
        hand: list[Card],
        top_card: Card | None,
        legal_moves: list[Card]
    ) -> Card | None:
        raise NotImplementedError("Subclasses need to implement this!")


    @staticmethod
    @abstractmethod
    def choose_suit(
        hand: list[Card],
    ) -> Suit:
        raise NotImplementedError("Subclasses need to implement this!")



class RandomStrategy(PlayerStrategy):
    # play a random card
    @staticmethod
    def play(
        hand: list[Card],
        top_card: Card | None,
        legal_moves: list[Card]
    ) -> Card | None:
        return random.choice(legal_moves) if legal_moves else None


    @staticmethod
    def choose_suit(
        hand: list[Card],
    ):
        return random.choice([suit for suit in Suit if suit is not Suit.JOKER])



class ScaredyStrategy(PlayerStrategy):
    @staticmethod
    def play(
        hand: list[Card],
        top_card: Card | None,
        legal_moves: list[Card]
    ) -> Card:
        # play the card worth most points
        return sorted(legal_moves, key=lambda card: card.value, reverse=True)[0]


    @staticmethod
    def choose_suit(
        hand: list[Card],
    ) -> Suit:
        # choose the suit where the player has the most points of in hand
        class SuitValues(NamedTuple):
            suit: Suit
            value: int
        return sorted(
            [
                SuitValues(
                    suit,
                    sum([card.value for card in hand if card.suit is suit]),
                ) for suit in Suit if suit is not Suit.JOKER
            ],
            key = lambda suit_values: suit_values.value,
            reverse = True
        )[0].suit