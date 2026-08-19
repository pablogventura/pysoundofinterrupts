"""CLI argparse and env defaults; no audio device or GUI."""
import sys

from pysoundofinterrupts import plot, sound


def _clear_sound_env(monkeypatch):
    for name in (
        "INTERRUPTS_AMPLITUDE",
        "INTERRUPTS_DIVIDER",
        "INTERRUPTS_SUBTRACTOR",
    ):
        monkeypatch.delenv(name, raising=False)


def _clear_plot_env(monkeypatch):
    for name in (
        "INTERRUPTS_PLOT_X_MAX",
        "INTERRUPTS_PLOT_Y_MAX",
        "INTERRUPTS_PLOT_INTERVAL",
    ):
        monkeypatch.delenv(name, raising=False)


def test_sound_parse_args_defaults(monkeypatch):
    _clear_sound_env(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["interrupts-sound"])
    args = sound._parse_args()
    assert args.amplitude == sound.DEFAULT_AMPLITUDE
    assert args.divider == sound.DEFAULT_DIVIDER
    assert args.subtractor == sound.DEFAULT_SUBTRACTOR


def test_sound_parse_args_cli(monkeypatch):
    _clear_sound_env(monkeypatch)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "interrupts-sound",
            "--amplitude",
            "0.5",
            "--divider",
            "10",
            "--subtractor",
            "100",
        ],
    )
    args = sound._parse_args()
    assert args.amplitude == 0.5
    assert args.divider == 10.0
    assert args.subtractor == 100.0


def test_sound_parse_args_env(monkeypatch):
    monkeypatch.setenv("INTERRUPTS_AMPLITUDE", "0.9")
    monkeypatch.setenv("INTERRUPTS_DIVIDER", "40")
    monkeypatch.setenv("INTERRUPTS_SUBTRACTOR", "200")
    monkeypatch.setattr(sys, "argv", ["interrupts-sound"])
    args = sound._parse_args()
    assert args.amplitude == 0.9
    assert args.divider == 40.0
    assert args.subtractor == 200.0


def test_plot_parse_args_defaults(monkeypatch):
    _clear_plot_env(monkeypatch)
    monkeypatch.setattr(sys, "argv", ["interrupts-plot"])
    args = plot._parse_args()
    assert args.x_max == plot.DEFAULT_X_MAX
    assert args.y_max == plot.DEFAULT_Y_MAX
    assert args.interval == plot.DEFAULT_INTERVAL_MS


def test_plot_parse_args_cli(monkeypatch):
    _clear_plot_env(monkeypatch)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "interrupts-plot",
            "--x-max",
            "20",
            "--y-max",
            "900",
            "--interval",
            "80",
        ],
    )
    args = plot._parse_args()
    assert args.x_max == 20
    assert args.y_max == 900
    assert args.interval == 80


def test_plot_parse_args_env(monkeypatch):
    monkeypatch.setenv("INTERRUPTS_PLOT_X_MAX", "12")
    monkeypatch.setenv("INTERRUPTS_PLOT_Y_MAX", "3000")
    monkeypatch.setenv("INTERRUPTS_PLOT_INTERVAL", "25")
    monkeypatch.setattr(sys, "argv", ["interrupts-plot"])
    args = plot._parse_args()
    assert args.x_max == 12
    assert args.y_max == 3000
    assert args.interval == 25
