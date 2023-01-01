from spoor import Spoor


def test_call_count():
    s = Spoor(attach=True)

    @s.track
    def target():
        pass

    target()
    assert s.call_count(target) == 1

    target()
    assert s.call_count(target) == 2


def test_called():
    s = Spoor(attach=True)

    @s.track
    def target():
        pass

    target()

    assert target.called is True


def test_not_called():
    s = Spoor(attach=True)

    @s.track
    def target():
        pass

    assert target.called is False


def test_lambda():
    s = Spoor(attach=True)

    target = lambda: ...  # noqa: E731
    target = s.track(target)

    target()

    assert target.called
    assert target.call_count == 1
