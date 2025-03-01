from abc import ABC, abstractmethod
import logging
from .Card import Card, Rank, Suit
from .Player import Player
import src.Game as Game # import like this to resolve circular import


class GameState(ABC):
    def __init__(self, game: Game):
        self.game = game

    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")




class CardPlayingState(GameState):
    def __init__(self, game, allow_pass):
        super().__init__(game)
        self.allow_pass = allow_pass # Whether the player can pass their turn without playing


    def execute(self):
        player: Player = self.game.get_current_player()
        previous_card: Card = self.game.get_previous_card()
        legal_moves: list[Card] = self.game.legal_moves(player, previous_card)

        card_played = player.play_card(previous_card, legal_moves)
        if card_played:
            self.game.process_played_card(player, card_played)
            logging.debug(f"Player {player.name} plays a {str(card_played)}. They have {len(player.hand)} cards left.")

            if not player.hand:
                self.game.round_winner = player
                # End the round
                return EndState(self.game)
            
            if card_played.is_special:
                return EffectState(self.game, card_played)
            
        elif not self.allow_pass:
            # if no card is played transition to drawing
            return DrawingState(self.game)
        
        # Transition to next player
        self.game.advance_play()
        return PlayingState(self.game)



class PlayingState(CardPlayingState):
    # State for when a player is playing a card
    def __init__(self, game):
        super().__init__(game, allow_pass=False)



class PostDrawState(CardPlayingState):
    # State for deciding if a drawn card can be played.
    def __init__(self, game):
        super().__init__(game, allow_pass=True)



class OptionalChainingState(CardPlayingState):
    # State for allowing the player to chain another card after playing a 10.
    def __init__(self, game):
        super().__init__(game, allow_pass=True)



class DrawingState(GameState):
    # State for when a player needs to draw a card
    def execute(self):
        player: Player = self.game.get_current_player()
        card: Card = player.draw_card(self.game.stack)
        logging.debug(f"Player {player.name} draws a card.")

        if card and self.game.is_legal_play(card, self.game.get_previous_card()):
            # Transition to allow playing the drawn card
            return PostDrawState(self.game)
        elif self.game.stack.size == 0:
            player.n_plays_to_skip += 1

        # Transition to next player
        self.game.advance_play()
        return PlayingState(self.game)



class EffectState(GameState):
    # State for handling effects of significant cards
    def __init__(self, game, card: Card):
        super().__init__(game)
        self.card: Card = card


    def execute(self):
        player: Player = self.game.get_current_player()

        if self.card.rank is Rank.ACE:
            for opponent in self.game.get_opponents(player):
                opponent.draw_card(self.game.stack)
            # Player must play another card
            return PlayingState(self.game)
        
        elif self.card.rank is Rank.TEN:
            self.game.change_direction()
            # Player may play another card
            return OptionalChainingState(self.game)
        
        elif self.card.rank is Rank.SEVEN or self.card.suit is Suit.JOKER:
            return ChainingEffectState(self.game, self.card)
        
        elif self.card.rank is Rank.JACK:
            suit = player.strategy.choose_suit()
            self.game.set_next_suit(suit)
            logging.debug(f"Player {player.name} wishes for {suit.value}.")

        # Transition to next Player
        self.game.advance_play()
        return PlayingState(self.game)



class ChainingEffectState(GameState):
    # State for handling effects of 7s and Jokers
    def __init__(self, game, card: Card):
        super().__init__(game)
        self.card: Card = card
        self.draw_count = 10 if card.suit is Suit.JOKER else 3


    def execute(self):
        next_player: Player = self.game.get_next_player()
        legal_moves = [card for card in next_player.hand if card.rank is self.card.rank]

        if legal_moves:
            card_played = next_player.play_card(self.card, legal_moves)
            if card_played:
                self.draw_count += 10 if card_played.suit is Suit.JOKER else 3
                self.game.process_played_card(next_player, card_played)
                logging.debug(f"Player {next_player.name} plays a {card_played}.")
                # Continue chaining
                return self
            
        else:
            logging.debug(f"Player {next_player.name} draws {self.draw_count} cards.")
            for _ in range(self.draw_count):
                next_player.draw_card(self.game.stack)

        # Transition to next player
        self.game.advance_play()
        return PlayingState(self.game)



class EndState(GameState):
    # State for handling when a player reaches 0 cards
    def __init__(self, game):
        super().__init__(game)


    def execute(self):
        print(f"Round Winner: {self.game.round_winner.name}")
        for player in self.game.players:
            player.tally_points()
            print(f"{player.name} - Points: {player.score}")

        # End the round
        return None