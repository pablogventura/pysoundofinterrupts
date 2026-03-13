# pysoundofinterrupts

[![PyPI version](https://badge.fury.io/py/pysoundofinterrupts.svg)](https://pypi.org/project/pysoundofinterrupts/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sonify and visualize Linux kernel interrupts by reading `/proc/interrupts`: listen to the system like a stethoscope or plot its activity in real time.

- **Course:** Used in the **Operating Systems** course (Sistemas Operativos) at **FaMAF–UNC** (Facultad de Matemática, Astronomía, Física y Computación, Universidad Nacional de Córdoba).
- **Credits:** Based on ideas by [Nicolás Wolovick](https://github.com/nwolovick): each interrupt drives the speaker in 1-bit PCM fashion (ZX-Spectrum style). If there are about 100 interrupts per second, you hear something like a 100 Hz tone.

**Linux only** — the program reads `/proc/interrupts`. On other systems it exits with a clear message.

**Links:** [PyPI](https://pypi.org/project/pysoundofinterrupts/) · [Repository](https://github.com/pablogventura/pysoundofinterrupts)

---

## Installation

### With pipx (recommended)

Install and run in an isolated environment without touching your global Python:

```bash
pipx install pysoundofinterrupts
```

This makes the `interrupts-sound` (audio) and `interrupts-plot` (graph) commands available.

To install from source (e.g. for development):

```bash
pipx install .
```

### With pip

```bash
pip install pysoundofinterrupts
```

Requirements: **Python 3.8+**, Linux.

---

## Usage

| Command            | Description                                                |
|--------------------|------------------------------------------------------------|
| `interrupts-sound` | Listen to kernel interrupts in real time (audio).          |
| `interrupts-plot`  | Real-time plot by type (LOC, RES, CAL, TLB).               |

### Real-time sound

```bash
interrupts-sound
```

Press Enter to exit. To calibrate the level:

| Option          | Environment variable      | Description                          |
|-----------------|----------------------------|--------------------------------------|
| `--subtractor`  | `INTERRUPTS_SUBTRACTOR`    | Subtract a floor from rate (default 1000) |
| `--divider`     | `INTERRUPTS_DIVIDER`       | Divide the rate (default 25)         |
| `--amplitude`   | `INTERRUPTS_AMPLITUDE`     | Volume 0–1 (default 0.2)            |

Example:

```bash
interrupts-sound --subtractor 800 --divider 20
```

### Real-time plot

```bash
interrupts-plot
```

Shows interrupts by type (LOC, RES, CAL, TLB). Options:

| Option        | Environment variable         | Description                          |
|---------------|-------------------------------|--------------------------------------|
| `--x-max`     | `INTERRUPTS_PLOT_X_MAX`       | Points on X axis (default 100)       |
| `--y-max`     | `INTERRUPTS_PLOT_Y_MAX`       | Y axis upper limit (default 5000)    |
| `--interval`  | `INTERRUPTS_PLOT_INTERVAL`    | Update interval in ms (default 50)   |

---

## Development and tests

Clone the repo, create an environment, and install in editable mode with test extras:

```bash
git clone https://github.com/pablogventura/pysoundofinterrupts.git
cd pysoundofinterrupts
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[test]"
pytest tests/ -v
```

---

## Publishing to PyPI

From the project directory, with [build](https://pypi.org/project/build/) and [twine](https://pypi.org/project/twine/) installed:

```bash
pip install build twine
./scripts/publish_to_pypi.sh
```

The first time, configure your PyPI credentials (token in `~/.pypirc` or `TWINE_USERNAME` and `TWINE_PASSWORD`). See [Twine: Configuration](https://twine.readthedocs.io/en/stable/#configuration).

---

## Troubleshooting

- **No audio:** Check your default output device. The program uses the system default or the first available output device.
- **Linux only:** On Windows or macOS the program exits stating it requires Linux.
- **Permissions:** Reading `/proc/interrupts` usually does not require root. If it fails, check that the file exists: `ls /proc/interrupts`.

---

## License

MIT. See [LICENSE](LICENSE) in the repository.
