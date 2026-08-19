"""Pulse synthesis and output-device selection (mocked sounddevice)."""
from types import SimpleNamespace

import numpy as np
import pytest

from pysoundofinterrupts.sound import _get_default_output_device, pulses_for_rate


def test_pulses_for_rate_silence_when_below_floor():
    buf = pulses_for_rate(
        frames=100,
        samplerate=1000.0,
        raw=500,
        subtractor=1000,
        divider=25,
        amplitude=0.2,
    )
    assert buf.shape == (100, 1)
    assert np.all(buf == 0)


def test_pulses_for_rate_clicks_when_rate_high():
    amplitude = 0.2
    buf = pulses_for_rate(
        frames=100,
        samplerate=100.0,
        raw=1000 + 25 * 50,
        subtractor=1000,
        divider=25,
        amplitude=amplitude,
    )
    # calibrated=50, duration=1s, pulse_count=50, step=2
    assert buf.shape == (100, 1)
    assert np.count_nonzero(buf) == 50
    assert buf[0, 0] == pytest.approx(255 * amplitude)
    assert buf[1, 0] == pytest.approx(0.0)


def test_get_default_output_device_none_picks_first_output(monkeypatch):
    from pysoundofinterrupts import sound

    monkeypatch.setattr(sound.sd, "default", SimpleNamespace(device=None))
    monkeypatch.setattr(
        sound.sd,
        "query_devices",
        lambda: [
            {"max_output_channels": 0},
            {"max_output_channels": 2},
        ],
    )
    assert _get_default_output_device() == 1


def test_get_default_output_device_tuple(monkeypatch):
    from pysoundofinterrupts import sound

    monkeypatch.setattr(sound.sd, "default", SimpleNamespace(device=(1, 4)))
    assert _get_default_output_device() == 4


def test_get_default_output_device_scalar(monkeypatch):
    from pysoundofinterrupts import sound

    monkeypatch.setattr(sound.sd, "default", SimpleNamespace(device=2))
    assert _get_default_output_device() == 2


def test_get_default_output_device_none_raises(monkeypatch):
    from pysoundofinterrupts import sound

    monkeypatch.setattr(sound.sd, "default", SimpleNamespace(device=None))
    monkeypatch.setattr(
        sound.sd,
        "query_devices",
        lambda: [{"max_output_channels": 0}],
    )
    with pytest.raises(RuntimeError, match="No audio output device"):
        _get_default_output_device()
