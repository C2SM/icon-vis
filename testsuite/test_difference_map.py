from utils import shell_cmd, file_exists, co_flag, plotting


def test_difference_map():
    plot_name = 'difference_map'

    # Check if co flag is working
    co_flag(plot_name)

    # Check if plotting works
    config_files = []
    input_files = []
    input_files_com = []
    plotting(plot_name, config_files, input_files, input_files_com)
