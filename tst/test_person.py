import pytest

from game import PersonView
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

    def test_radius(self):
        p = Person()
        v = PersonView(p, 0, 0)
        assert v.radius == pytest.approx(10.0)
