from spoor import Spoor


def test_name_function():
    s = Spoor()

    @s.track
    def target_one():
        pass

    @s.track
    def target_two():
        pass

    target_one()
    target_two()

    assert target_one.name == "target_one"
    assert target_two.name == "target_two"


def test_name_method():
    s = Spoor()

    @s.track
    class TargetClass:
        def method_one(self):
            pass

        def method_two(self):
            pass

    tc = TargetClass()

    assert tc.method_one.name == "TargetClass.method_one"
    assert tc.method_two.name == "TargetClass.method_two"


def test_name_method_no_instance():
    s = Spoor()

    @s.track
    class TargetClass:
        def method_one(self):
            pass

        def method_two(self):
            pass

    assert TargetClass.method_one.name == "TargetClass.method_one"
    assert TargetClass.method_two.name == "TargetClass.method_two"


def test_name_method_distinct_instances():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def method_one(self):
            pass

        def method_two(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.method_one()
    t2.method_one()

    assert t1.method_one.name == "t1.method_one"
    assert t1.method_two.name == "t1.method_two"
    assert t2.method_one.name == "t2.method_one"
    assert t2.method_two.name == "t2.method_two"


def test_name_method_groupped_instances():
    s = Spoor(distinct_instances=False)

    @s.track
    class TargetClass:
        def method_one(self):
            pass

        def method_two(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.method_one()
    t2.method_one()

    assert t1.method_one.name == "TargetClass.method_one"
    assert t2.method_two.name == "TargetClass.method_two"


def test_names_in_topn():
    s = Spoor()

    @s.track
    class TargetClass:
        def target_first(self):
            pass

        def target_second(self):
            pass

        def target_third(self):
            pass

    tc = TargetClass()
    tc.target_first()
    # _ = list([tc.target_first() for _ in range(2)])
    # _ = list([tc.target_second() for _ in range(10)])
    # _ = list([tc.target_third() for _ in range(15)])

    result = s.topn()
    print(result)
