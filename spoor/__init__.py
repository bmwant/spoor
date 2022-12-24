from functools import wraps

class Spoor:
    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            print("Wrapping", func)
            return func(*args, **kwargs)
        return inner



s = Spoor()

@s
def my_func():
    print("my_func is called")


my_func()