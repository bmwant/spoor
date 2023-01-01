from typing import Callable

from spoor import Spoor


def test_decorate_function_attached():
    s = Spoor(attach=True)

    def target():
        pass

    decorated = s._decorate_function(target)

    assert decorated is not target

    # check correct property assignment
    assert not hasattr(target, "called")
    assert not hasattr(target, "call_count")
    assert hasattr(decorated, "called")
    assert hasattr(decorated, "call_count")

    # check proper functools.wraps invocation
    assert hasattr(decorated, "__wrapped__")
    wrapped = decorated.__wrapped__
    assert target is wrapped

    assert isinstance(decorated, Callable)
    # NOTE: because we cannot set property on a function objects
    assert type(decorated) != type(target)


def test_decorate_function_not_attached():
    s = Spoor(attach=False)

    def target():
        pass

    decorated = s._decorate_function(target)

    assert decorated is not target

    # check correct property assignment
    assert not hasattr(target, "called")
    assert not hasattr(target, "call_count")
    assert not hasattr(decorated, "called")
    assert not hasattr(decorated, "call_count")

    # check proper functools.wraps invocation
    assert hasattr(decorated, "__wrapped__")
    wrapped = decorated.__wrapped__
    assert target is wrapped

    assert isinstance(target, Callable)
    assert isinstance(decorated, Callable)

    assert type(decorated) != type(target)
