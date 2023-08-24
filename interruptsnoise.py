#!/usr/bin/env python3
import sys
import time
import numpy as np
import sounddevice as sd

# Valores para calibración
amplitude = 0.2  # Volumen
divider = 25  # Divide la cantidad de interrupciones por segundo
substractor = 1000  # Sustrae un piso a la cantidad de interrupciones por segundo

device = sd.default.device[1]  # Dispositivo de salida predeterminado

samplerate = sd.query_devices(device, 'output')['default_samplerate'] / 10

def accumulated_interrupts():
    """
    Parser de /proc/interrupts para ver las interrupciones acumuladas
    """
    result = 0
    with open("/proc/interrupts", "r") as f:
        cpus = len(next(f).split())  # Cantidad de CPUs
        for line in f:
            line = line.split()
            if len(line) > cpus:
                try:
                    result += sum([int(i) for i in line[1:cpus+1]])
                except:
                    # Línea para descartar
                    continue
    return result

def intpersec():
    """
    Interrupciones por segundo, como es un generador hay que usarlo así:
    it = intpersec()    # Inicializo el generador 
    next(it)            # Obtengo el valor siguiente
    """
    last_interrupts = accumulated_interrupts()
    last_time = time.time()
    while True:
        current_interrupts = accumulated_interrupts()  # Medición actual
        current_time = time.time()
        amount = current_interrupts - last_interrupts
        period = current_time - last_time
        last_interrupts = current_interrupts
        last_time = current_time
        yield amount // period

def callback(outdata, frames, time, status):
    # Obtengo el valor de interrupciones calibradas
    j = (next(it) - substractor) / divider
    t = np.zeros(frames, dtype=np.uint8)
    t = t.reshape(-1, 1)
    tiempo = frames / samplerate  # Tiempo de audio que voy a generar
    j = int(j * tiempo)  # Interrupciones durante ese tiempo de audio
    
    if j <= 0 or int(frames/j) == 0:
        # Genero solo silencio si no hay interrupciones suficientes
        outdata[:] = amplitude * t
        return
    
    for i in range(0, len(t), int(frames/j)):
        t[i] = 255
    outdata[:] = amplitude * t

it = intpersec()

with sd.OutputStream(device=device, channels=1, callback=callback,
                     samplerate=samplerate):
    print('#' * 80)
    print('Para calibrar usar las variables divider y substractor del código')
    print('Presionar Enter para salir')
    print('#' * 80)
    input()
