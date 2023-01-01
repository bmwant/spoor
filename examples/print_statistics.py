import rich

from spoor import Spoor

s = Spoor()

# given


@s.track
def track_first(a: int, b: int) -> int:
    return a + b


@s.track
def track_second(a: float, b: float) -> float:
    return a / b


@s.track
def track_third():
    return {}


if __name__ == "__main__":
    # when
    track_first(2, 3)
    track_second(1.0, 5.0)
    track_second(2.1, 3.2)

    # then
    print(s.topn())
    rich.print(s.topn())
