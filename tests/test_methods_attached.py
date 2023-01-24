import pytest

from spoor import Spoor
from spoor.tracker import CallableWrapper


def test_exposed_properties():
    s = Spoor(attach=True)

    @s.track
    class TargetClass:
        def method(self):
            pass

    t1 = TargetClass()

    assert hasattr(t1.method, "called")
    assert hasattr(t1.method, "call_count")
    assert isinstance(t1.method, CallableWrapper)


def test_call_count():
    s = Spoor(attach=True)

    @s.track
    class TargetClass:
        def method(self):
            pass

    t1 = TargetClass()
    t1.method()
    assert t1.method.call_count == 1

    t1.method()
    assert t1.method.call_count == 2


def test_called():
    s = Spoor(attach=True)

    @s.track
    class TargetClass:
        def method(self):
            pass

    t1 = TargetClass()
    t1.method()

    assert t1.method.called is True


def test_not_called():
    s = Spoor(attach=True)

    @s.track
    class TargetClass:
        def method(self):
            pass

    t1 = TargetClass()

    assert t1.method.called is False


@pytest.mark.xfail(reason="Implement decoration of single unbound method")
def test_single_method_decoration():
    s = Spoor()

    # @s.track
    # def target():
    #     pass

    class TargetClass:
        @s.track
        def method_tracked(self):
            pass

        def method_not_tracked(self):
            pass

    t1 = TargetClass()

    t1.method_tracked()
    t1.method_not_tracked()
