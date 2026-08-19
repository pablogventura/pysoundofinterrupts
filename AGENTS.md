# Agent notes

Minimal guide for code agents. User-facing usage lives in `README.md`.

## Stack

- Python 3.10+, setuptools (`pyproject.toml`), Linux only (`/proc/interrupts`).
- Runtime: numpy, sounddevice, matplotlib.
- Tests: pytest (`[test]` extra). Publish: build + twine (`[dev]` extra).
- Package under `src/pysoundofinterrupts/` (`reader`, `sound`, `plot`).
- CLIs (pipx/pip entry points): `interrupts-sound`, `interrupts-plot`.

## Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"          # install (editable + tests)
# pip install -e ".[dev]"         # build + twine
# pipx install -e .               # isolated editable install; exposes CLIs
```

```bash
interrupts-sound                  # dev: audio (needs Linux + audio device)
interrupts-plot                   # dev: matplotlib plot
pytest tests/ -v                  # test (no audio/GUI)
python3 -m build                  # build sdist/wheel into dist/
./scripts/publish_to_pypi.sh      # build + twine upload
```

- lint: no detectado
- typecheck: no detectado
- migrate: no aplica

## Layout

```
src/pysoundofinterrupts/
  reader.py            # parse /proc/interrupts; rates
  sound.py             # CLI audio; pulses_for_rate
  plot.py              # CLI plot; append_capped (LOC, RES, CAL, TLB)
tests/
  conftest.py          # mock /proc fixtures
  test_interrupts_reader.py
  test_cli.py
  test_sound.py
  test_plot.py
  test_entry_points.py
scripts/publish_to_pypi.sh
pyproject.toml
requirements.txt
```

## Conventions

- English: code, comments, README, errors.
- Conventional Commits (`feat`, `fix`, `docs`, `test`, ...).
- Keep the `src/` layout and setuptools `packages.find` (`where = ["src"]`).
- Reader API (`pysoundofinterrupts.reader`): `accumulated_interrupts_*` (int totals), generators `intpersec_*`; injectable `interrupts_path` for tests.
- Keep `callback` / `animate` short; put pulse and window logic in `pulses_for_rate` and `append_capped`.
- Entry points: `pysoundofinterrupts.sound:main`, `pysoundofinterrupts.plot:main`.
- `_check_linux()` exits on non-Linux or missing `/proc/interrupts`.
- CLI defaults also via env: `INTERRUPTS_SUBTRACTOR`, `INTERRUPTS_DIVIDER`, `INTERRUPTS_AMPLITUDE`, `INTERRUPTS_PLOT_X_MAX`, `INTERRUPTS_PLOT_Y_MAX`, `INTERRUPTS_PLOT_INTERVAL`.
- Plot types default: `DEFAULT_INTERRUPT_TYPES` (`LOC`, `RES`, `CAL`, `TLB`).
- Parser: first line = CPU columns; skip non-numeric cells; IRQ name is `parts[0]` without trailing `:`.

## Tests

- Run all: `pytest tests/ -v`
- Run one: `pytest tests/test_interrupts_reader.py::test_accumulated_interrupts_total -v`
- Fixtures in `conftest.py` write mock `/proc/interrupts` (3 CPUs). Do not require a real `/proc` or audio/GUI.
- `pythonpath = ["src"]` in pytest config; import `pysoundofinterrupts.*` (no sys.path hacks).

## Do not

- Do not add lint/typecheck/CI configs unless asked; none exist.
- Do not target Windows/macOS for the CLIs; they must fail clearly via `_check_linux()`.
- Do not change `/proc/interrupts` parsing without updating the mock fixture and totals (see comments in the test).
- Do not put secrets in the repo; PyPI uses `~/.pypirc` or `TWINE_*`.
- Do not rewrite README for agent notes; keep this file short.
- Do not run `publish_to_pypi.sh` unless explicitly asked (uploads to PyPI).
- Do not assume Makefile, Docker, or GitHub Actions (none in this repo).
