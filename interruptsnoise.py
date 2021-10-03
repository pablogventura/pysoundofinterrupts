#!/usr/bin/env python3
import sys
import time
import numpy as np
import sounddevice as sd

# valores para calibracion
amplitude = 0.2  # volumen
divider = 25  # divide la cantidad de interrupciones por segundo
substractor = 1000  # sustrae un piso a la cantidad de interrupciones por segundo

device = sd.default.device[1]  # salida default

samplerate = sd.query_devices(device, 'output')['default_samplerate']


def accumulated_interrupts():
    """
    Parser de /proc/interrupts para ver las interrupciones acumuladas
    """
    result = 0
    with open("/proc/interrupts", "r") as f:
        cpus = len(next(f).split())  # cantidad de cpus
        for line in f:
            line = line.split()
            if len(line) > cpus:
                try:
                    result += sum([int(i) for i in line[1:-3]])
                except:
                    # linea para descartar
                    continue
    return result


def intpersec():
    """
    interrupciones por segundo, como es un generador hay que usarlo asi:
    next(intpersec())
    """
    last_interrupts = accumulated_interrupts()
    last_time = time.time()
    while True:
        current_interrupts = accumulated_interrupts()  # medicion actual
        current_time = time.time()
        amount = current_interrupts-last_interrupts
        period = current_time-last_time
        last_interrupts = current_interrupts
        last_time = current_time
        yield amount//period


def callback(outdata, frames, time, status):
    j = (next(intpersec())-substractor)/divider  # interrupciones calibradas
    t = np.zeros(frames, dtype=np.uint8)
    t = t.reshape(-1, 1)
    tiempo = frames/samplerate  # tiempo de audio que voy a generar
    j = int(j * tiempo)  # interrupciones durante ese tiempo de audio
    if j <= 0 or int(frames/j) == 0:
        # solo silencio
        outdata[:] = amplitude * t
        return

    for i in range(0, len(t), int(frames/j)):
        t[i] = 255
    outdata[:] = amplitude * t


with sd.OutputStream(device=device, channels=1, callback=callback,
                     samplerate=samplerate):
    print('#' * 80)
    print('Para calibrar usar las variables divider y substractor del codigo')
    print('Presionar Enter para salir')
    print('#' * 80)
    input()
