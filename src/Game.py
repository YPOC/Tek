from .Card import Card, Rank, Suit, BackColor
from .Deck import Deck
from .Stack import Stack
from .Player import Player
from .GameStates import PlayingState

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        self.round_winner: Player = None


    def setup_round(self):
        self.current_player_index = 0
        self.direction = 1
        self.stack = Stack([Deck(BackColor.BLUE), Deck(BackColor.RED)])
        self.stack.shuffle()
        self.discard_pile = []
        self.discard_pile.append(self.stack.draw()) # TODO: Remove
        for player in self.players: # TODO: Add cutting of cards and drawing special cards + clubs
            player.hand.clear()
            for _ in range(7):
                player.draw_card(self.stack)


    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]


    def get_next_player(self) -> Player:
        return self.players[(self.current_player_index + self.direction) % len(self.players)]


    def get_opponents(self, player: Player) -> list[Player]:
        return [p for p in self.players if p is not player]


    def get_previous_card(self) -> Card:
        return self.discard_pile[-1] if self.discard_pile else None


    def legal_moves(self, player: Player, previous_card: Card):
        return [card for card in player.hand if self.is_legal_play(card, previous_card)]


    def is_legal_play(self, card: Card, previous_card: Card) -> bool:
        if card.suit is Suit.JOKER:
            return True
        if card.suit is previous_card.suit or card.rank is previous_card.rank:
            return True
        if card.rank is Rank.JACK:
            return True
        return False


    def process_played_card(self, player: Player, card: Card) -> None:
        player.remove_card(card)
        self.discard_pile.append(card)


    def change_direction(self) -> None:
        self.direction *= -1


    def advance_play(self) -> None:
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)


    def set_next_suit(self, suit: Suit):
        # Set when wishing for a suit with a Jack
        self.next_suit = suit


    def play_round(self):
        self.setup_round()
        state = PlayingState(self)
        while state:
            state = state.execute()


    def play_game(self, n_rounds: int = 4):
        for _ in range(n_rounds):
            self.play_round()
            # print(f"Round Winner: {self.round_winner.name}")
            # for player in self.players:
            #     print(f"{player.name} - Points: {player.score}")