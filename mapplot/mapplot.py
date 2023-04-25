# Load required python packages
import argparse
import sys
from pathlib import Path

import cmcrameri.cm as cmc
import iconarray as iconvis  # import self-written modules from iconarray
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
        default="mapplot_output.png",
    )
    parser.add_argument("-co", action="store_true", help="get config options")
    args = parser.parse_args()

    #####################

    # B) Read config file or show available options

    #####################

    if args.co:
        print(
            "var, name (req): name of the variable as in the nc file\n"
            + "var, zname (req if the height dimension has a name other than height): Default: height\n"
            + "var, height (opt): index for height dimension (default 0 = ground level)\n"
            + "var, varlim (opt): lower and upper limit of color scale\n"
            + "var, grid_file (req if file is missing grid-information): path to grid file\n"
            + "var, time (opt): index/es of time variable (creates a range of plots between two given indexes divided by comma)\n"
            + "map, lonmin/lonmax/latmin/latmax (opt): values for map extension\n"
            + "map, projection (opt): projection to draw on (e.g., robin)\n"
            + "map, add_grid (opt): set false to remove grid with lat and lon labels\n"
            + "map, title (opt): title of plot\n"
            + "map, cmap (opt): name of colorbar\n"
            + "map, clabel (opt): label of colorbar\n"
            + "coord, name (opt): add markers at certain locations (several inputs possible)\n"
            + "coord, lon/lat (opt): lon and lat of the locations\n"
            + "coord, marker (opt): marker specifications for all locations\n"
            + "coord, marker_size (opt): marker sizes for all locations\n"
            + "coord, col (opt): colors of all markers for all locations"
        )
        sys.exit()

    # read config file
    var, map_c, coord, _ = iconvis.read_config(args.config_path)

    #############

    # C) Load data

    #############

    # Check if input file exists
    input_file = Path(args.input_file)
    if not input_file.is_file():
        sys.exit(args.input_file + " is not a valid file name")

    if iconvis.check_grid_information(input_file):
        ds = psy.open_dataset(input_file)
    elif "grid_file" in var.keys():
        ds = iconvis.combine_grid_information(input_file, var["grid_file"])
    else:
        sys.exit(
            "The file "
            + str(input_file)
            + " is missing the grid information. Please provide a grid file in the config."
        )

    #############

    # D) Plotting

    #############

    # Get map extension
    if "lonmin" not in map_c.keys():
        map_c["lonmin"] = min(np.rad2deg(ds.clon.values[:]))
    if "lonmax" not in map_c.keys():
        map_c["lonmax"] = max(np.rad2deg(ds.clon.values[:]))
    if "latmin" not in map_c.keys():
        map_c["latmin"] = min(np.rad2deg(ds.clat.values[:]))
    if "latmax" not in map_c.keys():
        map_c["latmax"] = max(np.rad2deg(ds.clat.values[:]))

    # Check if several time steps should be plotted
    if len(var["time"]) == 1:
        end_t = var["time"][0] + 1
    else:
        end_t = var["time"][1] + 1

    for i in range(var["time"][0], end_t):
        if "varlim" in var.keys():
            bounds = {
                "method": "minmax",
                "vmin": var["varlim"][0],
                "vmax": var["varlim"][1],
            }
        else:
            bounds = {
                "method": "minmax",
            }
        # create psyplot instance
        pp = ds.psy.plot.mapplot(name=var["name"])
        pp.update(
            t=i,
            bounds=bounds,
            map_extent=[
                map_c["lonmin"],
                map_c["lonmax"],
                map_c["latmin"],
                map_c["latmax"],
            ],
        )
        if "projection" in map_c.keys():
            pp.update(projection=map_c["projection"])
        if "add_grid" in map_c.keys():
            pp.update(xgrid=map_c["add_grid"], ygrid=map_c["add_grid"])
        if "title" in map_c.keys():
            pp.update(title=map_c["title"])
        if "cmap" in map_c.keys():
            pp.update(cmap=map_c["cmap"])
        else:
            pp.update(cmap=cmc.vik)
        if "clabel" in map_c.keys():
            pp.update(clabel=map_c["clabel"])
        # Check if height dimension exists
        # Check if variable has height as dimension and if the length of the dim is >1
        if var["zname"] in ds[var["name"]].dims and ds[var["name"]].sizes[var["zname"]]  > 1:
            pp.update(z=var["height"][0])
        else:
            print("Warning: The variable " + var["name"] + " doesn't have the height dimension " + var["zname"]+ ". Ignore this warning for 2D variables.")
        pp.update(borders=True, lakes=True, rivers=False)

        # go to matplotlib level
        fig = plt.gcf()

        if coord:
            llon = map_c["lonmax"] - map_c["lonmin"]
            llat = map_c["latmax"] - map_c["latmin"]
            for il in range(0, len(coord["lon"])):
                pos_lon, pos_lat = iconvis.add_coordinates(
                    coord["lon"][il],
                    coord["lat"][il],
                    map_c["lonmin"],
                    map_c["lonmax"],
                    map_c["latmin"],
                    map_c["latmax"],
                )
                fig.axes[0].plot(
                    pos_lon,
                    pos_lat,
                    coord["col"][il],
                    marker=coord["marker"][il],
                    markersize=coord["marker_size"][il],
                    transform=fig.axes[0].transAxes,
                )
                if "name" in coord.keys():
                    fig.axes[0].text(
                        pos_lon + llon * 0.003,
                        pos_lat + llat * 0.003,
                        coord["name"][il],
                        transform=fig.axes[0].transAxes,
                    )

        #############

        # E) Save figure

        #############

        # save figure
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if len(var["time"]) > 1:
            dot = "."
            pos_dot = args.output_file.find(dot)
            if pos_dot != -1:
                name_file = (
                    args.output_file[0:pos_dot]
                    + "_"
                    + str(i)
                    + args.output_file[pos_dot : len(args.output_file) + 1]
                )
            else:
                print(i)
                name_file = args.output_file + "_" + str(i)
        else:
            name_file = args.output_file
        output_file = Path(output_dir, name_file)
        print("The output is saved as " + str(output_file))
        plt.savefig(output_file)
