#!/usr/bin/env python3
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from interrupts_reader import (
    _check_linux,
    DEFAULT_INTERRUPT_TYPES,
    intpersec_by_type,
)

# Tipos de interrupciones y colores correspondientes
INTERR_TYPES = list(DEFAULT_INTERRUPT_TYPES)
COLORS = ["tab:red", "tab:blue", "tab:green", "tab:orange"]

DEFAULT_X_MAX = 100
DEFAULT_Y_MAX = 5000
DEFAULT_INTERVAL_MS = 50


def _parse_args():
    p = argparse.ArgumentParser(
        description="Gráfico en tiempo real de interrupciones por tipo (Linux, /proc/interrupts)."
    )
    p.add_argument(
        "--x-max",
        type=int,
        default=int(os.environ.get("INTERRUPTS_PLOT_X_MAX", DEFAULT_X_MAX)),
        help="Máximo de puntos en el eje X. Default: %s" % DEFAULT_X_MAX,
    )
    p.add_argument(
        "--y-max",
        type=int,
        default=int(os.environ.get("INTERRUPTS_PLOT_Y_MAX", DEFAULT_Y_MAX)),
        help="Límite superior del eje Y. Default: %s" % DEFAULT_Y_MAX,
    )
    p.add_argument(
        "--interval",
        type=int,
        default=int(os.environ.get("INTERRUPTS_PLOT_INTERVAL", DEFAULT_INTERVAL_MS)),
        help="Intervalo de actualización en ms. Default: %s" % DEFAULT_INTERVAL_MS,
    )
    return p.parse_args()


def main():
    _check_linux()
    args = _parse_args()
    x_max = args.x_max
    y_max = args.y_max
    interval_ms = args.interval

    it = intpersec_by_type(interrupt_types=INTERR_TYPES)

    def init_plot():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        interrupts = next(it)
        for j, line in enumerate(lines):
            y = list(line.get_ydata())
            if len(y) >= x_max:
                y.pop(0)
            y.append(interrupts[INTERR_TYPES[j]])
            line.set_data(range(len(y)), y)
        return lines

    fig = plt.figure()
    ax = plt.axes(xlim=(0, x_max), ylim=(0, y_max))
    lines = []
    for j in range(len(INTERR_TYPES)):
        line = ax.plot(
            [], [],
            ls="-",
            marker=".",
            color=COLORS[j],
            label=INTERR_TYPES[j],
        )[0]
        lines.append(line)

    anim = animation.FuncAnimation(
        fig,
        animate,
        frames=None,
        interval=interval_ms,
        blit=False,
        init_func=init_plot,
    )
    fig.legend()
    plt.show()


if __name__ == "__main__":
    main()
