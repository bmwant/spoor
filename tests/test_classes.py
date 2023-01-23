import pytest

from spoor import Spoor
from spoor.tracker import CallableWrapper


def test_call_count():
    s = Spoor()

    @s.track
    class TargetClass:
        def target_once(self):
            pass

        def target_twice(self):
            pass

    tc = TargetClass()
    tc.target_once()

    assert s.call_count(tc.target_once) == 1
    assert s.call_count(tc.target_twice) == 0

    tc.target_twice()
    tc.target_twice()

    assert s.call_count(tc.target_once) == 1
    assert s.call_count(tc.target_twice) == 2


def test_called():
    s = Spoor()

    @s.track
    class TargetClass:
        def target_called(self):
            pass

        def target_not_called(self):
            pass

    tc = TargetClass()
    tc.target_called()

    assert s.called(tc.target_called)
    assert not s.called(tc.target_not_called)


def test_dunder_is_not_tracked():
    s = Spoor()

    @s.track
    class TargetClass:
        def __str__(self):
            return "target class"

    tc = TargetClass()
    result = f"{tc}"  # noqa: F841

    assert not s.called(tc.__str__)


def test_dunder_is_tracked():
    s = Spoor(skip_dunder=False)

    @s.track
    class TargetClass:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

        def __bool__(self):
            return True

    t1 = TargetClass()
    t2 = TargetClass()

    result = t1 == t2
    assert result is False
    assert s.called(t1.__eq__)

    assert bool(t1) is True
    # NOTE: instances are groupped so method is considered the same
    assert s.called(t1.__bool__)
    assert s.called(t2.__bool__)

    assert s.called(t1.__init__)
    assert s.called(t2.__init__)


def test_dunder_with_distinct_instances():
    s = Spoor(skip_dunder=False, distinct_instances=True)

    @s.track
    class TargetClass:
        def __bool__(self):
            return False

    t1 = TargetClass()
    t2 = TargetClass()

    assert bool(t1) is False
    assert s.called(t1.__bool__)
    assert not s.called(t2.__bool__)


def test_distinct_instances():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()
    t3 = TargetClass()

    t1.target_called()

    assert hasattr(t1, "_spoor_name")
    assert hasattr(t2, "_spoor_name")
    assert hasattr(t3, "_spoor_name")
    assert t1._spoor_name == "t1"
    assert t2._spoor_name == "t2"
    assert t3._spoor_name == "t3"

    hash1 = hash(t1.target_called)
    hash2 = hash(t2.target_called)

    assert hash1 != hash2
    assert t1.target_called != t2.target_called

    assert s.called(t1.target_called)
    assert not s.called(t2.target_called)


def test_equality():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()
    t3 = TargetClass()

    t1.target_called()

    assert hasattr(t1, "_spoor_name")
    assert hasattr(t2, "_spoor_name")
    assert hasattr(t3, "_spoor_name")

    assert t1._spoor_name == "t1"
    assert t2._spoor_name == "t2"
    assert t3._spoor_name == "t3"

    hash1 = hash(t1.target_called)
    hash2 = hash(t2.target_called)
    hash3 = hash(t3.target_called)

    id1 = id(t1.target_called)
    id2 = id(t2.target_called)
    id3 = id(t3.target_called)

    # same wrapper is shared and then bound to an instance
    assert id1 == id2
    assert id2 == id3

    assert hash1 != hash2
    assert hash2 != hash3

    assert t1.target_called._func == t2.target_called._func
    assert t2.target_called._func == t3.target_called._func

    assert t1.target_called._bound_instance != t2.target_called._bound_instance
    assert t2.target_called._bound_instance != t3.target_called._bound_instance

    assert isinstance(t1.target_called, CallableWrapper)
    assert isinstance(t2.target_called, CallableWrapper)
    assert isinstance(t3.target_called, CallableWrapper)

    assert t1 is not t2
    assert t2 is not t3

    assert not (t2.target_called == t1.target_called)
    assert t1.target_called != t2.target_called

    assert s.called(t1.target_called)
    assert not s.called(t2.target_called)


def test_bound_methods():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    wrapper1 = t1.target_called
    wrapper2 = t2.target_called

    assert isinstance(wrapper1, CallableWrapper)
    assert isinstance(wrapper2, CallableWrapper)

    assert wrapper1 is not wrapper2
    assert id(wrapper1) != id(wrapper2)
    assert hash(wrapper1) != hash(wrapper2)

    assert hasattr(wrapper1, "_bound_instance")
    assert hasattr(wrapper2, "_bound_instance")
    bound1 = wrapper1._bound_instance
    bound2 = wrapper2._bound_instance

    assert bound1 is not bound2
    assert hash(wrapper1) == hash(bound1)
    assert hash(wrapper2) == hash(bound2)


@pytest.mark.parametrize("distinct_instances", [True, False])
def test_unbound_methods(distinct_instances):
    s = Spoor(distinct_instances=distinct_instances)

    @s.track
    class TargetClass:
        def target_called(self):
            return 42

    with pytest.raises(TypeError) as e:
        TargetClass.target_called()

    assert "missing 1 required positional argument: 'self'" in str(e)
    assert TargetClass.target_called(None) == 42
