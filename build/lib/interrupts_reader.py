#!/usr/bin/env python3
"""
Lectura de /proc/interrupts (solo Linux).

Formato esperado: primera línea con nombres de CPUs (columnas),
resto líneas "IRQ: n1 n2 n3 ..." con contadores por CPU.
Proporciona interrupciones acumuladas y generador de interrupciones por segundo.
"""
import sys
import time
from pathlib import Path

PROC_INTERRUPTS = Path("/proc/interrupts")

# Tipos de interrupción usados en el plot
DEFAULT_INTERRUPT_TYPES = ("LOC", "RES", "CAL", "TLB")


def _check_linux():
    """Comprueba que estamos en Linux; si no, termina con mensaje claro."""
    if sys.platform != "linux":
        sys.exit(
            f"Este programa solo funciona en Linux (lee /proc/interrupts). "
            f"Plataforma actual: {sys.platform}"
        )
    if not PROC_INTERRUPTS.exists():
        sys.exit(
            f"No se encuentra {PROC_INTERRUPTS}. ¿Estás en Linux?"
        )


def accumulated_interrupts_total(interrupts_path=PROC_INTERRUPTS):
    """
    Parsea /proc/interrupts y devuelve el total de interrupciones acumuladas
    (suma de todas las columnas de CPU para todas las filas numéricas).
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
    Parsea /proc/interrupts y devuelve un dict con las interrupciones acumuladas
    por tipo (claves: LOC, RES, CAL, TLB u las pasadas en interrupt_types).
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
    Generador infinito: yield de interrupciones por segundo (total).
    Si el periodo entre lecturas es 0 o muy pequeño, reutiliza el último valor.
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
    Generador infinito: yield de dict con interrupciones por segundo por tipo
    (LOC, RES, CAL, TLB). Si el periodo es 0 o muy pequeño, reutiliza el último.
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
