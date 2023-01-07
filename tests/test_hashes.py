import pytest

from spoor import Spoor


@pytest.mark.parametrize("distinct_instances", [True, False])
def test_hash_function(distinct_instances):
    s = Spoor(distinct_instances=distinct_instances)

    def target():
        pass

    decorated = s.track(target)

    assert id(target) != id(decorated)
    assert hash(target) == hash(decorated)
    assert decorated._func is target


@pytest.mark.parametrize("distinct_instances", [False])
def test_hash_unbound_method(distinct_instances):
    s = Spoor(distinct_instances=distinct_instances)

    class Target:
        def method(self):
            pass

    original = Target.method
    Target = s.track(Target)

    assert id(Target.method) != id(original)
    assert hash(Target.method) == hash(original)
    assert Target.method._func is original


def test_hash_disctinct_instances():
    s = Spoor(distinct_instances=True)

    class Target:
        def method(self):
            pass

    original = Target.method
    Target = s.track(Target)

    t1 = Target()
    t2 = Target()

    assert id(t1.method) != id(original)
    assert hash(t1.method) != hash(original)
    assert t1.method._func is original

    assert id(t2.method) != id(original)
    assert hash(t2.method) != hash(original)
    assert t2.method._func is original

    assert id(t1.method) != id(t2.method)  # different objects
    assert hash(t1.method) != hash(t2.method)  # different hashes
    assert t1.method._func is t2.method._func  # same underlying function


def test_hash_groupped_instances():
    s = Spoor(distinct_instances=False)

    class Target:
        def method(self):
            pass

    original = Target.method
    Target = s.track(Target)

    t1 = Target()
    t2 = Target()

    assert id(t1.method) != id(original)  # different objects
    assert hash(t1.method) == hash(original)  # but same hash to track
    assert t1.method._func is original

    assert id(t2.method) != id(original)
    assert hash(t2.method) == hash(original)
    assert t2.method._func is original

    assert id(t1.method) != id(t2.method)  # different bound methods
    assert hash(t1.method) == hash(t2.method)  # but same hash when groupped
    assert t1.method._func is t2.method._func  # same underlying function
