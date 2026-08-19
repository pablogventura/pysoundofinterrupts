"""Tests for the reader module using a mock /proc/interrupts file."""
from unittest.mock import patch

import pytest

from pysoundofinterrupts.reader import (
    accumulated_interrupts_total,
    accumulated_interrupts_by_type,
    intpersec_total,
    intpersec_by_type,
    DEFAULT_INTERRUPT_TYPES,
    _check_linux,
)

from conftest import MOCK_PROC_INTERRUPTS_LATER, MOCK_PROC_TOTAL


def test_accumulated_interrupts_total(mock_proc_file):
    total = accumulated_interrupts_total(mock_proc_file)
    # CPU0: 10+100+0+1000+50+10+1 = 1171; CPU1: 0+5+0+2000+60+20+2 = 2087; CPU2: 0+0+0+1500+70+30+3 = 1603
    # Total = 1171 + 2087 + 1603 = 4861 (ERR/short lines skipped)
    assert total == MOCK_PROC_TOTAL


def test_accumulated_interrupts_by_type(mock_proc_file):
    by_type = accumulated_interrupts_by_type(
        interrupt_types=list(DEFAULT_INTERRUPT_TYPES),
        interrupts_path=mock_proc_file,
    )
    assert by_type["LOC"] == 1000 + 2000 + 1500
    assert by_type["RES"] == 50 + 60 + 70
    assert by_type["CAL"] == 10 + 20 + 30
    assert by_type["TLB"] == 1 + 2 + 3
    assert all(isinstance(v, int) for v in by_type.values())


def test_accumulated_interrupts_by_type_missing_keys(mock_proc_file):
    by_type = accumulated_interrupts_by_type(
        interrupt_types=["FOO", "LOC"],
        interrupts_path=mock_proc_file,
    )
    assert by_type["FOO"] == 0
    assert by_type["LOC"] == 4500


def test_intpersec_total_yields_integers(mock_proc_file):
    gen = intpersec_total(interrupts_path=mock_proc_file, min_period=1e-6)
    v1 = next(gen)
    v2 = next(gen)
    assert isinstance(v1, int)
    assert isinstance(v2, int)


def test_intpersec_total_no_zerodiv(mock_proc_file):
    """Ensure period 0 does not cause ZeroDivisionError."""
    gen = intpersec_total(interrupts_path=mock_proc_file, min_period=1.0)
    with patch("pysoundofinterrupts.reader.time.time", side_effect=[0.0, 0.0]):
        v = next(gen)
    assert v == 0
    assert isinstance(v, int)


def test_intpersec_total_rate(mock_proc_path):
    times = iter([0.0, 1.0, 2.0])
    with patch(
        "pysoundofinterrupts.reader.time.time",
        side_effect=lambda: next(times),
    ):
        gen = intpersec_total(interrupts_path=mock_proc_path, min_period=1e-6)
        next(gen)
        mock_proc_path.write_text(MOCK_PROC_INTERRUPTS_LATER)
        rate = next(gen)
    # +200 over 1 second (IRQ1 +100, LOC +100)
    assert rate == 200


def test_intpersec_by_type_yields_dict(mock_proc_file):
    gen = intpersec_by_type(
        interrupt_types=list(DEFAULT_INTERRUPT_TYPES),
        interrupts_path=mock_proc_file,
        min_period=1e-6,
    )
    d = next(gen)
    assert set(d.keys()) == set(DEFAULT_INTERRUPT_TYPES)
    for k in DEFAULT_INTERRUPT_TYPES:
        assert isinstance(d[k], (int, float))


def test_intpersec_by_type_rate(mock_proc_path):
    times = iter([0.0, 1.0, 2.0])
    with patch(
        "pysoundofinterrupts.reader.time.time",
        side_effect=lambda: next(times),
    ):
        gen = intpersec_by_type(
            interrupt_types=list(DEFAULT_INTERRUPT_TYPES),
            interrupts_path=mock_proc_path,
            min_period=1e-6,
        )
        next(gen)
        mock_proc_path.write_text(MOCK_PROC_INTERRUPTS_LATER)
        rates = next(gen)
    assert rates["LOC"] == pytest.approx(100.0)
    assert rates["RES"] == pytest.approx(0.0)


def test_check_linux_rejects_non_linux(monkeypatch):
    monkeypatch.setattr("pysoundofinterrupts.reader.sys.platform", "darwin")
    with pytest.raises(SystemExit) as exc:
        _check_linux()
    assert "Linux" in str(exc.value)


def test_check_linux_missing_proc(monkeypatch, tmp_path):
    monkeypatch.setattr("pysoundofinterrupts.reader.sys.platform", "linux")
    missing = tmp_path / "no-such-proc"
    monkeypatch.setattr("pysoundofinterrupts.reader.PROC_INTERRUPTS", missing)
    with pytest.raises(SystemExit) as exc:
        _check_linux()
    assert "Not found" in str(exc.value)
