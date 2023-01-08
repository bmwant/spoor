from spoor import Spoor


def test_disabled():
    s = Spoor(disabled=True)

    @s.track
    def target():
        pass

    target()

    assert not s.called(target)
    assert s.call_count(target) == 0


def test_reenable():
    s = Spoor(disabled=False)

    @s.track
    def target():
        pass

    target()

    assert s.called(target)
    assert s.call_count(target) == 1

    s.disable()
    call_target = lambda: [target() for _ in range(5)]  # noqa: E731

    call_target()
    assert s.call_count(target) == 1

    s.enable()
    call_target()
    assert s.call_count(target) == 6


def test_get_key_is_same_for_groupped_instances():
    s = Spoor(distinct_instances=False)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    key1 = s._get_key(t1.target_called)
    key2 = s._get_key(t2.target_called)

    assert key1 == key2


def test_key_is_different_if_ungropped():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    key1 = s._get_key(t1.target_called)
    key2 = s._get_key(t2.target_called)

    assert key1 != key2


def test_get_key_on_functions():
    s = Spoor()

    def target_first():
        pass

    def target_second():
        pass

    key1 = s._get_key(target_first)
    key2 = s._get_key(target_second)

    assert key1 != key2


def test_key_stays_same_for_decorated_function():
    s = Spoor()

    def target():
        pass

    hash = s._get_key(target)
    decorated = s.track(target)

    new_hash = s._get_key(decorated)

    assert hash == new_hash


def test_key_stays_same_for_decorated_class():
    s = Spoor()

    class TargetClass:
        def target(self):
            pass

    hash = s._get_key(TargetClass.target)
    DecoratedClass = s.track(TargetClass)

    new_hash = s._get_key(DecoratedClass.target)

    assert hash == new_hash


def test_key_stays_same_for_decorated_instances():
    s = Spoor(distinct_instances=False)

    class TargetClass:
        def target(self):
            pass

    t1 = TargetClass()
    hash = s._get_key(t1.target)

    DecoratedClass = s.track(TargetClass)
    t2 = DecoratedClass()
    new_hash = s._get_key(t2.target)

    assert hash == new_hash


def test_is_tracked():
    s = Spoor()

    @s.track
    def target():
        pass

    @s.track
    class TargetClass:
        def target_first(self):
            pass

        def target_second(self):
            pass

    tc = TargetClass()

    assert s._is_tracked(target)
    assert s._is_tracked(TargetClass.target_first)
    assert s._is_tracked(TargetClass.target_second)
    assert s._is_tracked(tc.target_second)
    assert s._is_tracked(tc.target_second)


def test_is_not_tracked():
    s = Spoor()

    def target():
        pass

    class TargetClass:
        def target_first(self):
            pass

        def target_second(self):
            pass

    tc = TargetClass()

    assert not s._is_tracked(target)
    assert not s._is_tracked(TargetClass.target_first)
    assert not s._is_tracked(TargetClass.target_second)
    assert not s._is_tracked(tc.target_second)
    assert not s._is_tracked(tc.target_second)
