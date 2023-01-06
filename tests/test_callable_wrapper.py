from typing import Callable

from spoor import Spoor
from spoor.tracker import CallableWrapper


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


def test_both_attach_options():
    s_true = Spoor(attach=True)
    s_false = Spoor(attach=False)

    def target_true():
        pass

    def target_false():
        pass

    decorated_true = s_true._decorate_function(target_true)
    decorated_false = s_false._decorate_function(target_false)

    assert hasattr(decorated_true, "called")
    assert hasattr(decorated_true, "call_count")
    assert hasattr(decorated_true, "__wrapped__")

    assert hasattr(decorated_false, "__wrapped__")
    assert not hasattr(decorated_false, "called")
    assert not hasattr(decorated_false, "call_count")


def test_decoration_class_differs():
    s = Spoor()
    class_first = s._get_func_wrapper_cls()
    class_second = s._get_func_wrapper_cls()

    assert class_first is not class_second
    assert class_first.__name__ == class_second.__name__

    assert isinstance(class_first, type)
    assert isinstance(class_second, type)

    assert issubclass(class_first, CallableWrapper)
    assert issubclass(class_second, CallableWrapper)


def test_different_name_distinct_instances():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.target_called()
    t2.target_called()

    key1 = hash(t1.target_called)
    key2 = hash(t2.target_called)

    assert key1 != key2
    assert t1.target_called.name == "t1.target_called"
    assert t2.target_called.name == "t2.target_called"


def test_same_name_for_groupped_instances():
    s = Spoor(distinct_instances=False)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.target_called()
    t2.target_called()

    key1 = hash(t1.target_called)
    key2 = hash(t2.target_called)

    name1 = t1.target_called.name
    name2 = t1.target_called.name

    assert key1 == key2
    assert name1 == "TargetClass.target_called"
    assert name2 == "TargetClass.target_called"
