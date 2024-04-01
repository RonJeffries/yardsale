import pytest

from game import PersonView, scale_max
from person import Person


class TestPerson:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_person(self):
        p = Person()
        q = Person()
        p.transact(q, 1)
        assert p.wealth == 1100
        assert q.wealth == 900

    def test_person_q_wins(self):
        p = Person()
        q = Person()
        p.transact(q, 0)
        assert p.wealth == 900
        assert q.wealth == 1100

    def test_random(self):
        p = Person()
        q = Person()
        cycles = 10000
        wins = 0
        for i in range(cycles):
            p.wealth = 1000
            q.wealth = 1000
            p.transact(q)
            if p.wealth > q.wealth:
                wins += 1
        assert wins == pytest.approx(cycles/2, abs=cycles/20)

    def test_radius(self):
        p = Person()
        v = PersonView(p, 0, 0)
        assert v.radius == pytest.approx(10.0)

    def test_slice(self):
        wealths = [i for i in range(1000)]
        assert len(wealths) == 1000
        sliced = wealths[250:1000]
        assert len(sliced) == 750

    def test_scale(self):
        assert scale_max(500) == 1000
        assert scale_max(1000) == 2000
        assert scale_max(2000) == 5000
        assert scale_max(5000) == 10000
        assert scale_max(10000) == 20000
        assert scale_max(20000) == 50000
        assert scale_max(50000) == 100000

