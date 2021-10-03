#!/usr/bin/env python3
import sys
import time
import numpy as np
import sounddevice as sd

amplitude = 0.2
frequency = 440
device = sd.default.device[1]

start_idx = 0

samplerate = sd.query_devices(device, 'output')['default_samplerate']

log = []
piso = 0

def inst_interrupts():
    interrupts = 0

    with open("/proc/interrupts","r") as f:
        cpus = len(next(f).split())
        for line in f:
            line = line.split()
            if len(line) > cpus:
                try:
                    interrupts += sum([int(i) for i in line[1:-3]])
                except:
                    continue

    return interrupts

def intpsec():
    interrupts = inst_interrupts()
    last = time.time()
    while True:
        result = inst_interrupts()
        current = time.time()
        amount = result-interrupts
        period = current-last
        interruptspersecond=amount/period
        interrupts = result
        last = current
        log.append(interruptspersecond)
        yield int(interruptspersecond)

def callback(outdata, frames, time, status):
    j = next(intpsec())/10
    j -= piso
    #j=1
    t = np.zeros(frames)
    tiempo=frames/samplerate
    j = int(j * tiempo)
    t = t.reshape(-1, 1)

    if j <= 0 or int(frames/j) == 0:
        outdata[:] = amplitude * t
        return

    for i in range(0,len(t),int(frames/j)):
        t[i]=1
    outdata[:] = amplitude * t

with sd.OutputStream(device=device, channels=1, callback=callback,
                     samplerate=samplerate):
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    while True:
        input()
        piso = int(sum(log)/len(log))
        print("promedio %s" % piso)
