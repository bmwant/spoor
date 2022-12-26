import types
from functools import wraps
from typing import Optional, Callable, List

from varname import varname

from spoor.storage import Storage, MemoryStorage
from spoor.exporter import Exporter
from spoor.statistics import TopCalls


class Spoor:
    def __init__(
        self, 
        storage: Optional[Storage] = None,
        exporters: Optional[List[Exporter]] = None,
        attach: bool = False,
        distinct_instances: bool = False,
        disabled: bool = False,
    ):
        self.attach = attach
        if attach:
            raise NotImplemented("This feature is not implemented yet")
        self.distinct_instances = distinct_instances
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
            if self.distinct_instances:
                def new(cls, *args, **kwargs):
                    instance = object.__new__(cls)
                    instance._spoor_name = varname()
                    return instance
                setattr(target, "__new__", new)
            return self._decorate_methods(target)
        else:
            raise ValueError(f"Cannot track instance of {type(target)}")

    def _export(self):
        for e in self.exporters:
            pass
    
    def _decorate_function(self, func: Callable) -> Callable:
        # TODO: looks like callable is not specific enough
        # class with __call__ is also a callable
        @wraps(func)
        def inner(*args, **kwargs):
            if self.enabled:
                key = self._get_hash(inner)
                self.storage.set_name(key, inner.__name__)
                self.storage.inc(key)
                self._export()
            return func(*args, **kwargs)
        return inner

    def _decorate_method(self, func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            if self.enabled:
                self_ = args[0]
                method_name = inner.__name__
                class_name = self_.__class__.__name__
                alias = f"{class_name}.{method_name}"
                method = getattr(self_.__class__, method_name)
                if self.distinct_instances:
                    method = getattr(self_, method_name)
                    instance_name  = self_._spoor_name
                    alias = f"{instance_name}.{method_name}"

                key = self._get_hash(method)
                self.storage.set_name(key, alias)
                self.storage.inc(key)
                self._export()
            return func(*args, **kwargs)
        return inner

    def _is_dunder(self, name: str) -> bool:
        return (
            name.startswith("__") and
            name.endswith("__")
        )

    def _decorate_methods(self, klass):
        """
        These are not methods yet, there is no instance created to bound to
        """
        for key in klass.__dict__:
            method = klass.__dict__[key]
            if isinstance(method, types.FunctionType) and not self._is_dunder(key):
                decorated = self._decorate_method(method)
                setattr(klass, key, decorated)
                
        return klass
    
    def _get_hash(self, func_id):
        # TODO: add import by path
        if not self.distinct_instances:
            # NOTE: return same hash for different bound methods
            if hasattr(func_id, "__self__"):
                klass = func_id.__self__.__class__
                method = getattr(klass, func_id.__name__)
                return hash(method)
        return hash(func_id)

    def called(self, func_id) -> bool:
        return self.call_count(func_id) != 0

    def call_count(self, func_id):
        key = self._get_hash(func_id)
        return self.storage.get_value(key)

    def topn(self, n: int = 5) -> TopCalls:
        data = self.storage.most_common(top_n=n)
        return TopCalls(data)
