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

# import functools
# from threading import RLock

# def control(func):
#     control.lock = RLock()
#     print("control.x is", control.x)
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         with control.lock:
#             control.x += 1
#         return func(*args, **kwargs)

#     return inner

# control.x = 0


# @control
# def launch():
#     print("You can launch me in a thread, x is safe")

# print(control.x)

from varname import varname


class TargetClass:
    def __init__(self, name):
        self.name = name

    # def __new__(cls, *args, **kwargs):
    #     instance = super().__new__(cls)
    #     instance._name = "spoor name"
    #     return instance


def new(cls, *args, **kwargs):
    instance = object.__new__(cls)
    instance._name = varname()
    return instance


setattr(TargetClass, "__new__", new)


tc = TargetClass("name")
print(tc.name)
print(tc._name)

tc2 = TargetClass("another one")
print(tc2.name)
print(tc2._name)


from spoor import DatadogExporter, Spoor

s = Spoor(
    exporters=[DatadogExporter()],
)


del s
