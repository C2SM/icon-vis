from utils import co_flag, plotting


def test_difference_map():
    plot_name = "difference_map"

    # Check if co flag is working
    co_flag(plot_name)

    # Check if plotting works
    config_files = ["config_all_opt", "config_no_opt", "config_coord"]
    input_files = ["my_exp1_atm_3d_ml_20180921T000000Z"]
    input_files_com = ["my_exp1_diff"]
    plotting(plot_name, config_files, input_files, input_files_com)
