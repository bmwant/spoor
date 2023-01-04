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
