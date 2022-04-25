from utils import shell_cmd


def test_download_data():
    cmd = "python icon_vis/icon_vis/modules/get_data.py"
    status, _ = shell_cmd(cmd)

    assert status == 0, "Could not download data from ftp-server"
