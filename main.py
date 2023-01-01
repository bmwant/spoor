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


def wrap_with_inner(self):
    class Inner:
        def __init__(inner, func):
            inner.func = func

        def __call__(inner, *args, **kwargs):
            if self.enabled:
                key = self._get_hash(inner)
                alias = inner.__name__
                # logger.debug(f"Tracking {alias}[{key}]")
                self.storage.set_name(key, inner.__name__)
                self.storage.inc(key)
                self._export(alias)
            return inner.func(*args, **kwargs)

    setattr(Inner, "called", property(partial(self.called)))


def check_varname():
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


from functools import partial, wraps


class TargetClass:
    def one(self):
        print("one")

    @property
    def two(self):
        print("two")


def three(self):
    print("three")


class DS:
    def __get__(self, obj, objtype=None):
        return "three"


tc = TargetClass()
_three = partial(three, tc)
tc.three = DS()
# v = property(tc.three)
tc.one()
tc.two
print("type two is", type(getattr(tc, "two")))
# print("v is", v, type(v))
# breakpoint()
tc.three


def gta(obj, name):
    print("I am called")
    return obj.__getattribute__(name)


def original():
    print("I am untoched")


print(original.__getattribute__)


def fun():
    print("This is not fun")


fun.__getattribute__ = gta
fun.prop = DS()
setattr(fun, "prop", DS)
# breakpoint()
print(fun.prop)


class Inner:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def prop(self):
        return "three"


def decor(func):
    i = wraps(func)(Inner(func))
    print(i.__wrapped__)
    return i


def prop():
    print("I am a property")


def my_func():
    print("Just a function call")


my_func.prop = prop
my_func.prop  # prints 'I am a property'


my_func.__dict__["prop"] = property(lambda: "the prop")
print(my_func.prop)
