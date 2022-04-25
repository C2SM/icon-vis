# Load required python packages
import argparse
import sys
from pathlib import Path

import icon_vis.modules as iconvis  # import icon-vis self-written modules
import matplotlib.pyplot as plt
import numpy as np
import psyplot.project as psy

if __name__ == "__main__":

    ####################

    # A) Parsing arguments

    ####################

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", "-c", dest="config_path", help="path to config file"
    )
    parser.add_argument(
        "--infile", "-i", dest="input_file", help="path to input file", default=""
    )
    parser.add_argument(
        "--outdir", "-d", dest="output_dir", help="output directory", default=Path.cwd()
    )
    parser.add_argument(
        "--outfile",
        "-o",
        dest="output_file",
        help="name of output file",
        default="vertical_profile_output.png",
    )
    parser.add_argument("-co", action="store_true", help="get config options")

    args = parser.parse_args()

    #####################

    # B) Read config file or show available options

    #####################

    # Show options for config file
    if args.co:
        print(
            "var, name (req): name of variable as in nc file\n"
            + "var, time (opt): index of time variable. Default 0.\n"
            + "var, grid_file (req if file is missing grid-information): path to grid file\n"
            + "var, zname (req if data has height dimension called something other than height): Default: height\n"
            + "plot, xlabel/ylabel (opt): x and y labels\n"
            + "plot, title (opt): title of plot\n"
            + "plot, xlim/ylim (opt): lower and upper limit of x or y axis (two numbers needed)\n"
            + "coord, lon/lat (req if section coord): height profile of closest grid cell point (mean over whole map if not given)"
        )
        sys.exit()

    # read config file
    var, _, coord, plot = iconvis.read_config(args.config_path)

    #############

    # C) Load data

    #############

    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.is_file():
        sys.exit(args.input_file + " is not a valid file name")

    # load data
    if iconvis.check_grid_information(input_file):
        data = psy.open_dataset(input_file)
    elif "grid_file" in var.keys():
        data = iconvis.combine_grid_information(input_file, var["grid_file"])
    else:
        sys.exit(
            "The file "
            + str(input_file)
            + " is missing the grid information. Please provide a grid file in the config."
        )

    # variable and related things
    var_field = getattr(data, var["name"])
    var_dims = var_field.dims
    values = var_field.values

    # Check if time exists as dimension
    if "time" in var_dims:
        field_reduced = var_field.isel(time=var["time"][0])
    else:
        field_reduced = var_field

    # Get name of height dimension
    height_ind = [i for i, s in enumerate(var_dims) if var["zname"] in s]
    if height_ind:
        height_dim = var_dims[height_ind[0]]
        height = getattr(data, height_dim).values[:]
    if not height_ind or height.size == 1:
        sys.exit(
            "Could not find "
            + var["zname"]
            + " (altitude) dimension for "
            + var["name"]
            + "."
            + " Possible dimensions for "
            + var["name"]
            + " are: "
            + str(var_dims)
        )

    # Check if coordinates are given
    if coord:
        # convert from radians to degrees
        lats = np.rad2deg(data.clat.values[:])
        lons = np.rad2deg(data.clon.values[:])
        # Get cell index of closes cell
        ind = iconvis.ind_from_latlon(
            lats, lons, coord["lat"][0], coord["lon"][0], verbose=True
        )
        print(field_reduced.values.shape)
        values_red = field_reduced.values[:, ind]
    else:
        values_red = field_reduced.values.mean(axis=1)

    #############

    # D) Plot data

    #############

    f, axes = plt.subplots(1, 1)
    ax = axes
    h = ax.plot(values_red, height, lw=2)
    if "xlabel" in plot.keys():
        ax.set_xlabel(plot["xlabel"])
    if "ylabel" in plot.keys():
        ax.set_ylabel(plot["ylabel"])
    if "title" in plot.keys():
        ax.set_title(plot["title"])
    if "ylim" in plot.keys():
        plt.ylim(plot["ylim"])
    if "xlim" in plot.keys():
        plt.xlim(plot["xlim"])
    ax.axhline(0, color="0.1", lw=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    #############

    # E) Save figure

    #############

    output_dir = Path(args.output_dir)
    output_file = Path(output_dir, args.output_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("The output is saved as " + str(output_file))
    plt.savefig(output_file)
