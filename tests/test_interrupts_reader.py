"""
Tests for the interrupts_reader module using a mock /proc/interrupts file.
"""
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch

# Import from project root
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from interrupts_reader import (
    accumulated_interrupts_total,
    accumulated_interrupts_by_type,
    intpersec_total,
    intpersec_by_type,
    DEFAULT_INTERRUPT_TYPES,
)


# Typical /proc/interrupts content (3 CPUs)
MOCK_PROC_INTERRUPTS = """            CPU0       CPU1       CPU2
  0:         10          0          0  IRQ
  1:        100          5          0
  2:          0          0          0
LOC:      1000       2000       1500
RES:        50         60         70
CAL:        10         20         30
TLB:         1          2          3
"""


@pytest.fixture
def mock_proc_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(MOCK_PROC_INTERRUPTS)
        f.flush()
        path = Path(f.name)
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


def test_accumulated_interrupts_total(mock_proc_file):
    total = accumulated_interrupts_total(mock_proc_file)
    # CPU0: 10+100+0+1000+50+10+1 = 1171; CPU1: 0+5+0+2000+60+20+2 = 2087; CPU2: 0+0+0+1500+70+30+3 = 1603
    # Total = 1171 + 2087 + 1603 = 4861
    assert total == 4861


def test_accumulated_interrupts_by_type(mock_proc_file):
    by_type = accumulated_interrupts_by_type(
        interrupt_types=list(DEFAULT_INTERRUPT_TYPES),
        interrupts_path=mock_proc_file,
    )
    assert by_type["LOC"] == 1000 + 2000 + 1500
    assert by_type["RES"] == 50 + 60 + 70
    assert by_type["CAL"] == 10 + 20 + 30
    assert by_type["TLB"] == 1 + 2 + 3


def test_intpersec_total_yields_integers(mock_proc_file):
    gen = intpersec_total(interrupts_path=mock_proc_file, min_period=1e-6)
    v1 = next(gen)
    v2 = next(gen)
    assert isinstance(v1, int)
    assert isinstance(v2, int)


def test_intpersec_total_no_zerodiv(mock_proc_file):
    """Ensure period 0 does not cause ZeroDivisionError."""
    gen = intpersec_total(interrupts_path=mock_proc_file, min_period=1.0)
    with patch("interrupts_reader.time.time", side_effect=[0.0, 0.0]):
        v = next(gen)
    assert v == 0
    assert isinstance(v, int)


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
