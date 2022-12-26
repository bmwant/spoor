from spoor import Spoor


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
