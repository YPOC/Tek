from abc import ABC, abstractmethod
from collections import deque
import random

class ShufflingStrategy(ABC):
    @staticmethod
    @abstractmethod
    def shuffle(cards: deque):
        pass


class RandomShufflingStrategy(ShufflingStrategy):
    @staticmethod
    def shuffle(cards: deque):
        random.shuffle(cards)
