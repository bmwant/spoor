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
    pass


def test_hash_groupped_instances():
    pass
