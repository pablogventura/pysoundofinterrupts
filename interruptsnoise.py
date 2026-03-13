#!/usr/bin/env python3
import argparse
import os
import numpy as np
import sounddevice as sd

from interrupts_reader import _check_linux, intpersec_total

# Default calibration values (can be overridden via CLI or env)
DEFAULT_AMPLITUDE = 0.2
DEFAULT_DIVIDER = 25
DEFAULT_SUBTRACTOR = 1000

# Divisor of device samplerate: lowers sample rate so that
# interrupt "pulses" are audible (fewer samples per second).
SAMPLERATE_DIVISOR = 10


def _get_default_output_device():
    """Return the default output device in a robust way."""
    default = sd.default.device
    if default is None:
        # Pick the first available output device
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if dev.get("max_output_channels", 0) > 0:
                return i
        raise RuntimeError("No audio output device found.")
    if isinstance(default, (list, tuple)):
        return default[1] if len(default) > 1 else default[0]
    return default


def _parse_args():
    p = argparse.ArgumentParser(
        description="Sonify kernel interrupts (Linux, /proc/interrupts)."
    )
    p.add_argument(
        "--amplitude",
        type=float,
        default=float(os.environ.get("INTERRUPTS_AMPLITUDE", DEFAULT_AMPLITUDE)),
        help="Volume (0-1). Default: %s" % DEFAULT_AMPLITUDE,
    )
    p.add_argument(
        "--divider",
        type=float,
        default=float(os.environ.get("INTERRUPTS_DIVIDER", DEFAULT_DIVIDER)),
        help="Divide interrupts-per-second rate. Default: %s" % DEFAULT_DIVIDER,
    )
    p.add_argument(
        "--subtractor",
        type=float,
        default=float(os.environ.get("INTERRUPTS_SUBTRACTOR", DEFAULT_SUBTRACTOR)),
        help="Subtract a floor from interrupts/s rate. Default: %s" % DEFAULT_SUBTRACTOR,
    )
    return p.parse_args()


def main():
    _check_linux()
    args = _parse_args()
    amplitude = args.amplitude
    divider = args.divider
    subtractor = args.subtractor

    device = _get_default_output_device()
    info = sd.query_devices(device, "output")
    base_samplerate = info["default_samplerate"]
    samplerate = base_samplerate / SAMPLERATE_DIVISOR

    it = intpersec_total()

    def callback(outdata, frames, time_info, status):
        if status:
            print(status, flush=True)
        raw = next(it)
        j = (raw - subtractor) / divider
        t = np.zeros(frames, dtype=np.uint8)
        t = t.reshape(-1, 1)
        duration = frames / samplerate
        j = int(j * duration)
        step = int(frames / j) if j > 0 else 0
        if j <= 0 or step <= 0:
            outdata[:] = amplitude * t
            return
        for i in range(0, len(t), step):
            t[i] = 255
        outdata[:] = amplitude * t

    with sd.OutputStream(
        device=device,
        channels=1,
        callback=callback,
        samplerate=samplerate,
    ):
        print("#" * 80)
        print("Calibrate with: --subtractor, --divider, --amplitude (or INTERRUPTS_* env vars)")
        print("Press Enter to exit")
        print("#" * 80)
        input()


if __name__ == "__main__":
    main()
