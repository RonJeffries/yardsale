from random import random


class Person:
    def __init__(self):
        self.wealth = 1000

    def bet(self):
        return 0.1*self.wealth

    def transact(self, other, prob=None):
        prob = prob if prob is not None else random()
        bet = min(self.bet(), other.bet())
        if prob > 0.5:
            self.wealth += bet
            other.wealth -= bet
        else:
            other.wealth += bet
            self.wealth -= bet


