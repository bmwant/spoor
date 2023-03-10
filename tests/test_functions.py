from spoor import Spoor


def test_call_count():
    s = Spoor()

    @s.track
    def target():
        pass

    target()
    assert s.call_count(target) == 1

    target()
    assert s.call_count(target) == 2


def test_called():
    s = Spoor()

    @s.track
    def target():
        pass

    target()

    assert s.called(target) is True


def test_not_called():
    s = Spoor()

    @s.track
    def target():
        pass

    assert s.called(target) is False


def test_lambda():
    s = Spoor()

    target = lambda: ...  # noqa: E731
    target = s.track(target)

    target()

    assert s.called(target)
    assert s.call_count(target) == 1
