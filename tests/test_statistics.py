from spoor import Spoor


def test_most_common():
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
    print(result)
