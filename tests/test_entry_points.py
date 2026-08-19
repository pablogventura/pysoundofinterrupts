"""Package entry points are importable (editable install)."""
from importlib.metadata import entry_points

from pysoundofinterrupts.plot import main as plot_main
from pysoundofinterrupts.sound import main as sound_main


def test_cli_mains_are_callable():
    assert callable(sound_main)
    assert callable(plot_main)


def test_console_script_entry_points():
    selected = entry_points().select(group="console_scripts")
    by_name = {ep.name: ep.value for ep in selected}
    assert by_name.get("interrupts-sound") == "pysoundofinterrupts.sound:main"
    assert by_name.get("interrupts-plot") == "pysoundofinterrupts.plot:main"
