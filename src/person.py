from random import random


class Person:
    def __init__(self):
        self._wealth = 1000
        self.min_wealth = self.wealth
        self.max_wealth = self.wealth

    @property
    def wealth(self):
        return self._wealth

    @wealth.setter
    def wealth(self, value):
        self._wealth = value
        self.min_wealth = min(self.min_wealth, value)
        self.max_wealth = max(self.max_wealth, value)

    def bet(self):
        return 0.1*self.wealth

    def transact(self, other, prob=None):
        prob = prob if prob is not None else random()
        # bet = min(self.bet(), other.bet())
        if prob > 0.5:
            self.wealth += other.bet()
            other.wealth -= other.bet()
        else:
            other.wealth += self.bet()
            self.wealth -= self.bet()


