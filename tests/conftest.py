"""Shared fixtures: mock /proc/interrupts without a live kernel."""
import pytest

# Typical /proc/interrupts content (3 CPUs). Total of all CPU cells = 4861.
MOCK_PROC_INTERRUPTS = """            CPU0       CPU1       CPU2
  0:         10          0          0  IRQ
  1:        100          5          0
  2:          0          0          0
LOC:      1000       2000       1500
RES:        50         60         70
CAL:        10         20         30
TLB:         1          2          3
ERR:        not a number
short
"""

MOCK_PROC_TOTAL = 4861

# Same file with +100 on IRQ 1 CPU0 and +100 on LOC CPU0 (total 5061).
MOCK_PROC_INTERRUPTS_LATER = """            CPU0       CPU1       CPU2
  0:         10          0          0  IRQ
  1:        200          5          0
  2:          0          0          0
LOC:      1100       2000       1500
RES:        50         60         70
CAL:        10         20         30
TLB:         1          2          3
"""


@pytest.fixture
def mock_proc_file(tmp_path):
    path = tmp_path / "interrupts"
    path.write_text(MOCK_PROC_INTERRUPTS)
    return path


@pytest.fixture
def mock_proc_path(tmp_path):
    """Writable mock path for rate tests that change file contents."""
    path = tmp_path / "interrupts"
    path.write_text(MOCK_PROC_INTERRUPTS)
    return path
