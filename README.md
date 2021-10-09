The Sounds of Interrupts - Python Version
=========================================

Idea
----

Originally implemented in C by Nicolás Wolovick with the idea that each interrupt drives a speaker in a 1-bit PCM fashion as on the ZX-Spectrum.
This would lead to discover how OS interacts with the world. Some kind of stethoscope for learning how the OS behaves.
Then if there are 100 interruptions per second you should hear something like a 100Hz tone.

Install
-------
To run the script you need Python 3 and Pip. To install the dependencies run in your shell:
```
pip install -r requirements.txt
```

Run
---

Run ```python interruptsnoise.py``` to listen to interrupts, or ```python interruptsplot.py``` to see the real-time plot of interrupts.

To calibrate the noise level you can modify the variables ```subtractor``` and ```divider``` in the code.
