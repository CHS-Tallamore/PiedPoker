from typing import List

from card_internals.rank import Rank
from player.player import Player
from probability.base_poker_event import BasePokerEvent
from round.round_result import RoundResult


class PlayerHasCardRanks(BasePokerEvent):
    def __init__(self, target_ranks: List[Rank], player: Player = None):
        """
        Checks whether the player has ALL of the target Ranks in their 2 dealt cards
        :type target_ranks: List[Rank]
        :param player: Optional, if empty, defaults to first player in game
        :type player: Player
        """
        super().__init__()
        self.player = player
        self.target_ranks = target_ranks

    def is_event(self, round_result: RoundResult) -> bool:
        if not self.player:
            self.player = round_result.player_one
        actual_cards = round_result.player_during_round[self.player].cards
        set_intersection = set(self.target_ranks).intersection(set([c.rank for c in actual_cards]))
        return len(set_intersection) == len(set(self.target_ranks))

    def __str__(self):
        return f'{self.__class__.__name__}: {self.target_ranks}'

    def __repr__(self):
        return str(self)
