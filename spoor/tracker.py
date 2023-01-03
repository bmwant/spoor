import operator
import types
import typing
from abc import ABC
from collections import deque
from functools import wraps
from typing import Callable, List, Optional, Union

from varname import varname

from spoor.exporter import Exporter
from spoor.statistics import FuncCall, TopCalls
from spoor.storage import MemoryStorage, Storage
from spoor.utils import logger


class CallableWrapper(ABC):
    pass


# NOTE: at runtime, isinstance(x, T) will raise TypeError
WrapperType = typing.TypeVar("WrapperType", bound=CallableWrapper)


class Spoor:
    def __init__(
        self,
        storage: Optional[Storage] = None,
        exporters: Optional[List[Exporter]] = None,
        attach: bool = False,
        distinct_instances: bool = False,
        skip_dunder: bool = True,
        disabled: bool = False,
    ):
        self.attach = attach
        self.distinct_instances = distinct_instances
        self.skip_dunder = skip_dunder
        self._disabled = disabled
        self.storage = storage or MemoryStorage()
        self.exporters = exporters or []

    @property
    def enabled(self) -> bool:
        return not self._disabled

    def enable(self):
        self._disabled = False

    def disable(self):
        self._disabled = True

    def track(self, target):
        if isinstance(target, types.FunctionType):
            return self._decorate_function(target)
        elif isinstance(target, type):
            if self.attach:
                raise NotImplementedError("Attach for methods does not work yet")

            if self.distinct_instances:

                def new(cls, *args, **kwargs):
                    instance = object.__new__(cls)
                    instance._spoor_name = varname()
                    return instance

                setattr(target, "__new__", new)
            return self._decorate_methods(target)
        else:
            # TODO: add track by import path
            raise ValueError(f"Cannot track instance of {type(target)}")

    def _export(self, key: str):
        for e in self.exporters:
            e.send(key=key)

    def __getitem__(self, func_id: Union[Callable, str]) -> FuncCall:
        key = self._get_hash(func_id)
        try:
            call_count = self.storage.get_value(key)
            func_call = FuncCall(
                name=self.storage.get_name(key),
                called=bool(call_count),
                call_count=call_count,
            )
            return func_call
        except KeyError:
            raise KeyError(f"{func_id.__name__} is not tracked")

    def __del__(self):
        """
        Flush all the exporters
        """
        logger.debug("Flusing all the exporters and garbage collection")
        deque(
            map(operator.methodcaller("flush"), self.exporters),
            maxlen=0,
        )

    def _get_func_wrapper_cls(self, is_method: bool = False) -> WrapperType:
        """
        NOTE: We cannot attach a property on a function object,
        so class-based callable wrapper is used instead
        """
        spoor = self

        class Wrapper(CallableWrapper):
            """
            NOTE: should be nested class to be able expose properties on some
            wrapped objects and hide on others
            """

            def __init__(instance, func: Callable):
                instance._func = func
                instance._bound_instance = None

            def _bound(self, instance):
                self._bound_instance = instance

            def __call__(instance, *args, **kwargs):
                self_ = instance._bound_instance
                if spoor.enabled:
                    if is_method:
                        method_name = instance.__name__
                        class_name = self_.__class__.__name__
                        alias = f"{class_name}.{method_name}"
                        method = getattr(self_.__class__, method_name)
                        if spoor.distinct_instances:
                            method = getattr(self_, method_name)
                            instance_name = self_._spoor_name
                            alias = f"{instance_name}.{method_name}"
                        key = spoor._get_hash(method)
                    else:
                        alias = instance.__name__
                        key = spoor._get_hash(instance)
                    logger.debug(f"Tracking {alias}[{key}]")
                    # TODO: set name on initial register step
                    spoor.storage.set_name(key, alias)
                    spoor.storage.inc(key)
                    spoor._export(alias)

                if is_method:
                    return instance._func(self_, *args, **kwargs)
                return instance._func(*args, **kwargs)

            def __get__(self, instance, cls):
                self._bound(instance)
                return self

            def __hash__(self):
                if spoor.distinct_instances:
                    return hash(self._bound_instance)
                return hash(self._func)

        return Wrapper

    def _decorate_function(self, func: Callable, is_method: bool = False) -> Callable:
        WrapperClass = self._get_func_wrapper_cls(is_method=is_method)
        inner = wraps(func)(WrapperClass(func))
        if self.attach:
            setattr(inner.__class__, "called", property(self.called))
            setattr(inner.__class__, "call_count", property(self.call_count))

        return inner

    def _is_dunder(self, name: str) -> bool:
        return name.startswith("__") and name.endswith("__")

    def _is_tracked(self, func_id) -> bool:
        return isinstance(func_id, CallableWrapper) and issubclass(
            func_id.__class__, CallableWrapper
        )

    def _decorate_methods(self, klass):
        """
        These are not methods yet, there is no instance created to bound to
        """
        for key in klass.__dict__:
            method = klass.__dict__[key]
            skip_method = self.skip_dunder and self._is_dunder(key)
            if isinstance(method, types.FunctionType) and not skip_method:
                logger.debug(f"Wrapping method {method}")
                decorated = self._decorate_function(method, is_method=True)
                setattr(klass, key, decorated)

        return klass

    def _get_hash(self, func_id):
        if not self.distinct_instances:
            # NOTE: return same hash for different bound methods
            if hasattr(func_id, "__self__"):
                klass = func_id.__self__.__class__
                method = getattr(klass, func_id.__name__)
                return hash(method)
        return hash(func_id)

    def called(self, func_id) -> bool:
        return self.call_count(func_id) != 0

    def call_count(self, func_id) -> int:
        key = self._get_hash(func_id)
        count = self.storage.get_value(key)
        logger.debug(f"Calls count {func_id.__name__}[{key}] = {count}")
        return count

    def topn(self, n: int = 5) -> TopCalls:
        data = self.storage.most_common(top_n=n)
        return TopCalls(data)
