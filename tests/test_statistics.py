import rich

from spoor import Spoor
from spoor.statistics import TopCalls


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
    assert result[0] == ('TargetClass.target_thrice', 3)


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
    assert result[0] == ('TargetClass.target_thrice', 3) 
    assert result[-1] == ('TargetClass.target_once', 1) 


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
