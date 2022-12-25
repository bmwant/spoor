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
    pass


def test_dunder_is_not_tracked():
    s = Spoor()

    @s.track
    class TargetClass:
        def __str__(self):
            return "target class"

    tc = TargetClass()
    result = f"{tc}"

    assert not s.called(tc.__str__)