"""Sliding-window helper for the live plot (no matplotlib window)."""
from pysoundofinterrupts.plot import append_capped


def test_append_capped_grows_until_limit():
    series = []
    series = append_capped(series, 1.0, x_max=3)
    series = append_capped(series, 2.0, x_max=3)
    series = append_capped(series, 3.0, x_max=3)
    assert series == [1.0, 2.0, 3.0]


def test_append_capped_drops_oldest():
    series = [1.0, 2.0, 3.0]
    series = append_capped(series, 4.0, x_max=3)
    assert series == [2.0, 3.0, 4.0]
