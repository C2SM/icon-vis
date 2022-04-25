from utils import co_flag, file_exists, plotting, shell_cmd


def test_mapplot():
    plot_name = "mapplot"

    # Check if co flag is working
    co_flag(plot_name)

    # Check if plotting works
    config_files = ["config_all_opt", "config_no_opt", "config_coord"]
    input_files = ["my_exp1_atm_3d_ml_20180921T000000Z", "lfff01000000"]
    plotting(plot_name, config_files, input_files)
