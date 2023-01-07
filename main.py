# class MyClass:
#     def my_method(self):
#         print(f"Called bounded to {self}")


# m_unbound = MyClass.my_method
# print(f"{type(m_unbound)} {hash(m_unbound)}")  # <class 'function'> 8783579798336
# m_unbound(None)

# mc = MyClass()
# m1 = mc.my_method
# print(f"{type(m1)} {hash(m1)}")  # <class 'method'> 122173
# m1()

# m2 = mc.my_method
# print(f"{type(m2)} {hash(m2)}")  # <class 'method'> 122173
# m2()

# print(m1 == m2)  # True
# print(m1 is m2)  # False
# print(id(m1) == id(m2))  # False


# print(m1.__self__ is m2.__self__)  # True
# print(m1.__func__ is m2.__func__)  # True
# print(m2.__func__ is m_unbound)  # True


# class FunctionLike:
#     def __init__(self, func, instance=None):
#         self.im_func = func
#         self.im_self = instance

#     def __call__(self, *args, **kwargs):
#         if self.im_self is not None:
#             # inject `self` as a first argument
#             args = (self.im_self, ) + args

#         return self.im_func(*args, **kwargs)


#     def __get__(self, instance, cls):
#         if instance is not None:
#             # bind method to instance
#             # NOTE: also creating new object each time
#             return FunctionLike(func=self.im_func, instance=instance)

#         return self

#     def __eq__(self, other):
#         return (self.im_func, self.im_self) == (other.im_func, other.im_self)


# def target(self=None):
#     print(f"Bound to {self}")

# unbound = FunctionLike(target)
# unbound()

# class MyClass: pass

# MyClass.my_method = unbound

# mc = MyClass()

# m1 = mc.my_method
# m1()

# m2 = mc.my_method
# m2()

# print(m1 == m2)  # True
# print(m1 is m2)  # False
# print(id(m1) == id(m2))  # False


# print(m1.im_self is m2.im_self)  # True
# print(m1.im_func is m2.im_func)  # True
# print(m2.im_func is target)  # True
