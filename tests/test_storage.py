from spoor import Spoor


def test_get_value():
    s = Spoor()

    @s.track
    def target():
        pass

    target()

    key = hash(target)
    result = s.storage.get_value(key)
    assert result == 1
