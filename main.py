# s = MagicProxyLib()

# @s
# class MyClass:

#     def not_called(self):
#         print("This is not called")

#     def first_method(self):
#         print("First is called")

#     def second_method(self):
#         print("Second is called")


# mc = MyClass()
# mc.first_method()
# mc.second_method()
# mc.second_method()


# assert not s.called(mc.not_called)
# assert s.called(mc.first_method)
# assert s.call_count(mc.second_method) == 2

import functools
from threading import RLock

def control(func):
    control.lock = RLock()
    print("control.x is", control.x)
    @functools.wraps(func)
    def inner(*args, **kwargs):
        with control.lock:
            control.x += 1
        return func(*args, **kwargs)
    
    return inner

control.x = 0


@control
def launch():
    print("You can launch me in a thread, x is safe")

print(control.x)