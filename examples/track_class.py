from spoor import Spoor

s = Spoor()

# given


@s.track
class TrackClass:
    def method_first(self, a: int, b: int) -> int:
        return a + b

    def method_second(self, a: float, b: float) -> float:
        return a / b

    def method_third(self):
        return {}


if __name__ == "__main__":
    # when
    tc = TrackClass()
    tc.method_first(2, 3)
    tc.method_second(1.0, 5.0)
    tc.method_second(2.1, 3.2)

    # then
    assert s.called(tc.method_first)
    assert s.called(tc.method_second)
    assert not s.called(tc.method_third)

    assert s.call_count(tc.method_first) == 1
    assert s.call_count(tc.method_second) == 2
    assert s.call_count(tc.method_third) == 0
