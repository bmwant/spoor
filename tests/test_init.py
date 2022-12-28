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
