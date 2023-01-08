class MyClass:
    def method(self):
        print("Calling me")


m1 = MyClass.method


instance = MyClass()
m2 = instance.method
print(m2.__self__.__class__)  # <class 'MyClass'>

print(m1.__qualname__)  # 'MyClass.method'
