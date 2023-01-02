from spoor import Spoor


def test_disabled():
    pass


def test_reenable():
    pass


def test_get_hash_is_same_for_groupped_instances():
    s = Spoor(distinct_instances=False)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    key1 = s._get_hash(t1.target_called)
    key2 = s._get_hash(t2.target_called)

    assert key1 == key2


def test_hash_is_different_if_ungropped():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    key1 = s._get_hash(t1.target_called)
    key2 = s._get_hash(t2.target_called)

    assert key1 != key2


def test_get_hash_on_functions():
    s = Spoor()

    def target_first():
        pass

    def target_second():
        pass

    key1 = s._get_hash(target_first)
    key2 = s._get_hash(target_second)

    assert key1 != key2


def test_hash_stays_same_for_decorated_function():
    s = Spoor()

    def target():
        pass

    hash = s._get_hash(target)
    decorated = s.track(target)

    new_hash = s._get_hash(decorated)

    assert hash == new_hash


def test_hash_stays_same_for_decorated_class():
    s = Spoor()

    class TargetClass:
        def target(self):
            pass

    hash = s._get_hash(TargetClass.target)
    DecoratedClass = s.track(TargetClass)

    new_hash = s._get_hash(DecoratedClass.target)

    assert hash == new_hash


def test_hash_stays_same_for_decorated_instances():
    s = Spoor(distinct_instances=False)

    class TargetClass:
        def target(self):
            pass

    t1 = TargetClass()
    hash = s._get_hash(t1.target)

    DecoratedClass = s.track(TargetClass)
    t2 = DecoratedClass()
    new_hash = s._get_hash(t2.target)

    assert hash == new_hash
