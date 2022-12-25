from functools import wraps
from typing import Optional


from spoor.broker import Broker, MemoryBroker


class Spoor:
    def __init__(
        self, 
        broker: Optional[Broker] = None,
        attach: bool = False,
    ):
        self.attach = attach
        self.broker = broker or MemoryBroker()
    
    def track(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = self._get_hash(inner)
            self.broker.inc(key)
            return func(*args, **kwargs)
        return inner

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