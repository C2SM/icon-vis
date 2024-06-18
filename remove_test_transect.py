from utils import shell_cmd


def test_transect():
    status, _ = shell_cmd("python transect/plot_icon_transects.py")
    assert status == 0, "psy-transect does not run"
