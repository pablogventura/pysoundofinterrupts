#!/usr/bin/env python3
"""
Read /proc/interrupts (Linux only).

Expected format: first line with CPU names (columns),
remaining lines "IRQ: n1 n2 n3 ..." with per-CPU counters.
Provides accumulated interrupts and interrupts-per-second generators.
"""
import sys
import time
from pathlib import Path

PROC_INTERRUPTS = Path("/proc/interrupts")

# Interrupt types used in the plot
DEFAULT_INTERRUPT_TYPES = ("LOC", "RES", "CAL", "TLB")


def _check_linux():
    """Check we are on Linux; if not, exit with a clear message."""
    if sys.platform != "linux":
        sys.exit(
            f"This program only runs on Linux (it reads /proc/interrupts). "
            f"Current platform: {sys.platform}"
        )
    if not PROC_INTERRUPTS.exists():
        sys.exit(
            f"Not found: {PROC_INTERRUPTS}. Are you on Linux?"
        )


def accumulated_interrupts_total(interrupts_path=PROC_INTERRUPTS):
    """
    Parse /proc/interrupts and return total accumulated interrupts
    (sum of all CPU columns for all numeric rows).
    """
    result = 0
    with open(interrupts_path, "r") as f:
        cpus = len(next(f).split())
        for line in f:
            parts = line.split()
            if len(parts) <= cpus:
                continue
            try:
                result += sum(int(x) for x in parts[1 : cpus + 1])
            except (ValueError, IndexError):
                continue
    return result


def accumulated_interrupts_by_type(
    interrupt_types=None,
    interrupts_path=PROC_INTERRUPTS,
):
    """
    Parse /proc/interrupts and return a dict of accumulated interrupts
    by type (keys: LOC, RES, CAL, TLB or those passed in interrupt_types).
    """
    if interrupt_types is None:
        interrupt_types = DEFAULT_INTERRUPT_TYPES
    result = {t: 0.0 for t in interrupt_types}
    with open(interrupts_path, "r") as f:
        cpus = len(next(f).split())
        for line in f:
            parts = line.split()
            if len(parts) <= cpus:
                continue
            irq_type = parts[0].strip(":")
            if irq_type not in result:
                continue
            try:
                result[irq_type] = sum(
                    float(x) for x in parts[1 : cpus + 1]
                )
            except (ValueError, IndexError):
                continue
    return result


def intpersec_total(interrupts_path=PROC_INTERRUPTS, min_period=1e-6):
    """
    Infinite generator: yields interrupts per second (total).
    If the period between reads is 0 or very small, reuses the last value.
    """
    last_total = accumulated_interrupts_total(interrupts_path)
    last_time = time.time()
    last_rate = 0
    while True:
        current_total = accumulated_interrupts_total(interrupts_path)
        current_time = time.time()
        period = current_time - last_time
        last_time = current_time
        if period >= min_period:
            last_rate = int((current_total - last_total) / period)
        last_total = current_total
        yield last_rate


def intpersec_by_type(
    interrupt_types=None,
    interrupts_path=PROC_INTERRUPTS,
    min_period=1e-6,
):
    """
    Infinite generator: yields dict of interrupts per second by type
    (LOC, RES, CAL, TLB). If period is 0 or very small, reuses the last.
    """
    if interrupt_types is None:
        interrupt_types = DEFAULT_INTERRUPT_TYPES
    last = accumulated_interrupts_by_type(interrupt_types, interrupts_path)
    last_time = time.time()
    last_rates = {k: 0.0 for k in interrupt_types}
    while True:
        current = accumulated_interrupts_by_type(
            interrupt_types, interrupts_path
        )
        current_time = time.time()
        period = current_time - last_time
        last_time = current_time
        if period >= min_period:
            last_rates = {
                k: (current[k] - last[k]) / period
                for k in interrupt_types
            }
        last = current.copy()
        yield last_rates.copy()
