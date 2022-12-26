import types
from functools import wraps
from typing import Optional, Callable, List

from spoor.storage import Storage, MemoryStorage
from spoor.exporter import Exporter


class Spoor:
    def __init__(
        self, 
        storage: Optional[Storage] = None,
        exporters: Optional[List[Exporter]] = None,
        attach: bool = False,
        group: bool = False,
        disabled: bool = False,
    ):
        self.attach = attach
        self.group = group
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
            return self._decorate_methods(target)
        else:
            raise ValueError(f"Cannot track instance of {type(target)}")

    def _decorate_function(self, func: Callable) -> Callable:
        # TODO: looks like callable is not specific enough
        # class with __call__ is also a callable
        @wraps(func)
        def inner(*args, **kwargs):
            if self.enabled:
                key = self._get_hash(inner)
                self.broker.inc(key)
            return func(*args, **kwargs)
        return inner

    def _decorate_method(self, func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            if self.enabled:
                self_ = args[0]
                method_name = inner.__name__
                method = getattr(self_, method_name)
                # TODO: check flag for per-instance tracking
                key = self._get_hash(method)
                self.broker.inc(key)
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
        return hash(func_id)

    def called(self, func_id) -> bool:
        return self.call_count(func_id) != 0

    def call_count(self, func_id):
        key = self._get_hash(func_id)
        return self.broker.get_value(key)



def main():
    s = Spoor()

    @s.track
    def my_func():
        print("my_func is called")

    my_func()
    print()


if __name__ == "__main__":
    main()
