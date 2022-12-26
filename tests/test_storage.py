from spoor import Spoor


def test_get_name_function():
    s = Spoor()

    @s.track
    def target():
        pass

    target()

    key = s._get_hash(target)
    result = s.storage.get_name(key)
    assert result == "target"


def test_same_name_for_groupped_instances():
    s = Spoor(distinct_instances=False)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.target_called()
    t2.target_called()

    key1 = s._get_hash(t1.target_called)
    key2 = s._get_hash(t2.target_called)

    result1 = s.storage.get_name(key1)
    result2 = s.storage.get_name(key2)

    assert key1 == key2
    assert result1 == "TargetClass.target_called"   
    assert result2 == "TargetClass.target_called"


def test_different_name_distinct_instances():
    s = Spoor(distinct_instances=True)

    @s.track
    class TargetClass:
        def target_called(self):
            pass

    t1 = TargetClass()
    t2 = TargetClass()

    t1.target_called()
    t2.target_called()

    key1 = s._get_hash(t1.target_called)
    key2 = s._get_hash(t2.target_called)
    result1 = s.storage.get_name(key1)
    result2 = s.storage.get_name(key2)

    assert key1 != key2
    assert result1 == "t1.target_called"
    assert result2 == "t2.target_called"
