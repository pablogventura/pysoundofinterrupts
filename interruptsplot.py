#!/usr/bin/env python3
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Tipos de interrupciones y colores correspondientes
interr_types = [
    'LOC',      # Interrupciones locales del temporizador
    'RES',      # Interrupciones de reprogramación
    'CAL',      # Interrupciones de llamadas de función
    'TLB'       # Invalidaciones de TLB
]

colors = [
    'tab:red',
    'tab:blue',
    'tab:green',
    'tab:orange'
]

x_max = 100
y_max = 5000

def accumulated_interrupts():
    """
    Parser de /proc/interrupts para ver las interrupciones acumuladas
    """
    result = {}
    with open("/proc/interrupts", "r") as f:
        cpus = len(next(f).split())  # Cantidad de CPUs
        for line in f:
            line = line.split()
            interrupt_t = line[0].strip(":")
            if interrupt_t in interr_types:
                try:
                    result[interrupt_t] = sum(
                            [float(i) for i in line[1:cpus+1]])
                except:
                    # Línea para descartar
                    continue
    return result

def intpersec():
    """
    Interrupciones por segundo, como es un generador hay que usarlo así:
    it = intspersec()   # Para inicializar
    next(it)            # Para obtener el siguiente valor
    """
    last_interrupts = accumulated_interrupts()
    last_time = time.time()
    while True:
        current_interrupts = accumulated_interrupts()  # Medición actual
        current_time = time.time()
        period = current_time - last_time
        last_time = current_time
        result = { k: (current_interrupts[k] - last_interrupts[k]) / period
            for k in interr_types
        }
        last_interrupts = current_interrupts.copy()
        yield result

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
        y.append(interrupts[interr_types[j]])
        line.set_data(range(len(y)), y)
    return lines

it = intpersec()

fig = plt.figure()
ax = plt.axes(xlim=(0, x_max), ylim=(0, y_max))
lines = []
for j in range(len(interr_types)):
    line = ax.plot([], [],
            ls='-', marker='.', color=colors[j], label=interr_types[j])[0]
    lines.append(line)

anim = animation.FuncAnimation(fig, animate,
        frames=None, interval=50, blit=False, init_func=init_plot)
fig.legend()
plt.show()