import pytest
import rich

from spoor import Spoor
from spoor.statistics import FuncCall, TopCalls


def test_most_common():
    # TODO: move to storage tests
    s = Spoor()

    @s.track
    class TargetClass:
        def target_once(self):
            pass

        def target_twice(self):
            pass

        def target_thrice(self):
            pass

    tc = TargetClass()

    tc.target_once()

    tc.target_twice()
    tc.target_twice()

    tc.target_thrice()
    tc.target_thrice()
    tc.target_thrice()

    result = s.storage.most_common()
    assert result[0] == ("TargetClass.target_thrice", 3)


def test_top_n():
    s = Spoor()

    @s.track
    class TargetClass:
        def target_once(self):
            pass

        def target_twice(self):
            pass

        def target_thrice(self):
            pass

    tc = TargetClass()

    tc.target_once()

    tc.target_twice()
    tc.target_twice()

    tc.target_thrice()
    tc.target_thrice()
    tc.target_thrice()

    result = s.topn(n=3)

    assert len(result) == 3
    assert result[0] == ("TargetClass.target_thrice", 3)
    assert result[-1] == ("TargetClass.target_once", 1)


def test_rich_render(capsys):
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
    _ = list([tc.target_first() for _ in range(5)])
    _ = list([tc.target_second() for _ in range(10)])
    _ = list([tc.target_third() for _ in range(15)])

    result = s.topn()
    assert isinstance(result, TopCalls)

    rich.print(result)

    output = capsys.readouterr().out
    assert "Name" in output
    assert "TargetClass" in output
    assert "15" in output


def test_get_item():
    s = Spoor()

    @s.track
    def target():
        pass

    target()
    func_call = s[target]

    assert isinstance(func_call, FuncCall)
    assert func_call.called is True
    assert func_call.call_count == 1
    assert func_call.name == "target"


@pytest.mark.skip(reason="strict is not implemented yet")
def test_get_item_missing_strict():
    s = Spoor()

    @s.track
    def target():
        pass

    def missing():
        pass

    with pytest.raises(KeyError):
        s[missing]


def test_get_item_missing_not_strict():
    s = Spoor()

    @s.track
    def target():
        pass

    def missing():
        pass

    result = s[missing]

    assert isinstance(result, FuncCall)
    # NOTE: just default values
    assert result.name == ""
    assert result.called is False
    assert result.call_count == 0


def test_func_call_render_called(capsys):
    fc = FuncCall(name="function", called=True, call_count=5)
    rich.print(fc)

    output = capsys.readouterr().out
    assert "function" in output
    assert "5 calls" in output


def test_func_call_render_not_called(capsys):
    fc = FuncCall(name="function")
    rich.print(fc)

    output = capsys.readouterr().out
    assert output == "• function\n"
