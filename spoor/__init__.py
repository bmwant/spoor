from functools import wraps
from collections import Counter

class Spoor:
    def __init__(self, attach: bool = False):
        self.attach = attach
        # TODO: add lock for thread safety
        self._registry = Counter()
    
    def track(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            func_hash = self._get_hash(inner)
            self._registry[func_hash] += 1
            return func(*args, **kwargs)
        return inner

    def _get_hash(self, func_id):
        return hash(func_id)

    def called(self, func_id) -> bool:
        return self.call_count(func_id) != 0

    def call_count(self, func_id):
        func_hash = self._get_hash(func_id)
        return self._registry[func_hash]



def main():
    s = Spoor()

    @s.track
    def my_func():
        print("my_func is called")

    my_func()
    print()


if __name__ == "__main__":
    main()