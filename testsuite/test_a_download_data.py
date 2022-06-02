import iconarray as iconvis  # import icon-vis self-written modules


def test_download_data():
    try:
        iconvis.get_example_data()
    except Exception:
        raise AssertionError(
            "get_example_data() raised Exception! Could not download data from ftp-server"
        )
