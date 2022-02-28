from typing import List

from card_internals.card import Card
from card_internals.rank import Rank
from card_internals.suit import Suit

import numpy as np


class Deck:
    ALL_CARDS = np.array([Card(rank, suit) for rank in Rank.ALLOWED_VALUES_SET for suit in Suit.ALLOWED_VALUES])

    def __init__(self, excluding: List[Card] = ()):
        self.excluded_cards = set(excluding) if excluding else set()

    def draw(self, n=1):
        if n == 0:
            return []

        if n > len(self.ALL_CARDS) - len(self.excluded_cards):
            raise RuntimeError(f'Error: Cannot draw {n} cards from a deck with only {len(self.ALL_CARDS) - len(self.excluded_cards)} un-drawn cards.')

        drawn_cards = []
        selected_cards = np.random.choice(self.ALL_CARDS, size=n, replace=True)

        for c in selected_cards:
            # Doing it this way so we can reuse the same list for the deck of cards without having to reinitialize it
            # for every simulation which has proven to be very costly
            # Since, even in the biggest poker table with 9 players, there will only ever be 23 cards drawn from the
            # deck, we can safely assume this function will suffice for the task
            if c in self.excluded_cards:
                pass
            else:
                self.excluded_cards.add(c)
                drawn_cards.append(c)

        return drawn_cards + self.draw(n - len(drawn_cards))

    def shuffle(self, excluding: List[Card] = ()):
        """
        Shuffles the deck, with the option to exclude any cards that have already been drawn
        :param excluding:
        :type excluding:
        :return:
        :rtype:
        """
        self.excluded_cards = set(excluding) if excluding else set()

    def __eq__(self, other):
        return self.excluded_cards == other.excluded_cards
