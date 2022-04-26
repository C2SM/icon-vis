import os.path


def update_config(config_dictionary_instance):
    modified_config = config_dictionary_instance
    modified_config["data_dir"] = os.path.join(os.environ.get("CONDA_PREFIX"),
                                               "cartopy")
    return modified_config
