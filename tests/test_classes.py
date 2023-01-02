from spoor import Spoor


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

    t1.target_called()

    assert hasattr(t1, "_spoor_name")
    assert hasattr(t2, "_spoor_name")
    assert t1._spoor_name == "t1"
    assert t2._spoor_name == "t2"

    hash1 = s._get_hash(t1.target_called)
    hash2 = s._get_hash(t2.target_called)

    assert hash1 != hash2
    assert s.called(t1.target_called)
    assert not s.called(t2.target_called)
