# Load required python packages
import argparse
import sys
from pathlib import Path

import icon_vis.modules as iconvis  # import icon-vis self-written modules
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import psyplot.project as psy
import xarray as xr

if __name__ == "__main__":

    ####################

    # A) Parsing arguments

    ####################

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", "-c", dest="config_path", help="path to config file"
    )
    parser.add_argument(
        "--infile",
        "-i",
        dest="input_file",
        help="path to input file or folder containing .nc files",
        default="",
    )
    parser.add_argument(
        "--outdir", "-d", dest="output_dir", help="output directory", default=Path.cwd()
    )
    parser.add_argument(
        "--outfile",
        "-o",
        dest="output_file",
        help="name of output file",
        default="timeseries_output.png",
    )
    parser.add_argument("-co", action="store_true", help="get config options")
    args = parser.parse_args()

    #####################

    # B) Read config file or show available options

    #####################

    if args.co:
        print(
            "var, name (req): name of variable as in nc file\n"
            + "var, height (opt): index of height dimension (default 0)\n"
            + "var, unc (opt): add uncertainty to plot (only available option std=standard deviation)\n"
            + "var, grid_file (req if file is missing grid-information): path to grid file\n"
            + "var, zname (req if data has height dimension other than height): Default: height\n"
            + "plot, xlabel/ylabel (opt): x and y labels\n"
            + "plot, title (opt): title of plot\n"
            + "plot, xlim (opt): start end end time\n"
            + "plot, ylim (opt): lower and upper limit of y axis\n"
            + "plot, date_format (opt): date format (needs two % after each other)\n"
            + "coord, lon/lat (opt): height profile of closest grid cell point (mean over whole map if not given)"
        )
        sys.exit()

    # read config file
    var, _, coord, plot = iconvis.read_config(args.config_path)

    #############

    # C) Load data

    #############

    # load data
    input_file = Path(args.input_file)
    if input_file.is_dir():
        data = xr.open_mfdataset(str(Path(input_file, "*.nc")), engine="netcdf4")
    elif input_file.is_file():
        data = psy.open_dataset(input_file)
    else:
        sys.exit(args.input_file + " is not a valid file or directory name")

    if not iconvis.check_grid_information(data):
        if "grid_file" in var.keys():
            data = iconvis.add_grid_information(input_file, var["grid_file"])
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
    if "time" not in var_dims:
        sys.exit("Only one timestep given. No timeseries can be plotted.")
    else:
        time = data.time.values[:]

    # Check if height exists as dimension
    if var["zname"] in var_field.dims[1]:
        values_red = values[:, var["height"][0], :]
    else:
        values_red = values

    # Check if coordinates are given
    if coord:
        # convert from radians to degrees
        lats = np.rad2deg(data.clat.values[:])
        lons = np.rad2deg(data.clon.values[:])
        # Get cell index of closes cell
        ind = iconvis.ind_from_latlon(
            lats, lons, coord["lat"][0], coord["lon"][0], verbose=True
        )
        values_red = values_red[:, ind]
    else:
        values_red = values_red.mean(axis=1)

    #############

    # D) Plotting

    #############

    # plot settings
    f, axes = plt.subplots(1, 1)
    ax = axes
    # plot uncertainty
    if "unc" in var.keys():
        if var["unc"] == "std":
            var_std = values_red.std(axis=0)
            ax.fill_between(
                time, values_red - var_std, values_red + var_std, color="#a6bddb"
            )

    h = ax.plot(time, values_red, lw=2)
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

    myFmt = mdates.DateFormatter(plot["date_format"])
    ax.xaxis.set_major_formatter(myFmt)
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
