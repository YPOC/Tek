from abc import ABC, abstractmethod
from collections import deque
import random

from .Card import Card

class ShufflingStrategy(ABC):
    @staticmethod
    @abstractmethod
    def shuffle(cards: deque[Card]):
        pass


class RandomShufflingStrategy(ShufflingStrategy):
    @staticmethod
    def shuffle(cards: deque[Card]):
        random.shuffle(cards)
