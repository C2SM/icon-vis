import pathlib

import numpy as np
import psyplot.project as psy
import six
import xarray as xr


class WrongGridException(Exception):
    def __init__(
        self,
        grid,
        message="""It looks like this grid you are trying to merge could be wrong. There are no dimensions in the data with {cells} cells or {edges} edges. """,
    ):
        self.grid = grid
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message.format(
            cells=self.grid.dims["cell"], edges=self.grid.dims["edge"]
        )


def add_cell_encoding(obj):
    try:
        if "clat" not in obj.encoding["coordinates"]:
            obj.encoding["coordinates"] += " clat"
        if "clon" not in obj.encoding["coordinates"]:
            obj.encoding["coordinates"] += " clon"
    except Exception:
        obj.encoding["coordinates"] = "clon clat"


def add_edge_encoding(obj):
    try:
        if "elat" not in obj.encoding["coordinates"]:
            obj.encoding["coordinates"] += " elat"
        if "elon" not in obj.encoding["coordinates"]:
            obj.encoding["coordinates"] += " elon"
    except Exception:
        obj.encoding["coordinates"] = "elon elat"


def check_grid_information(file):
    if isinstance(file, pathlib.PurePath) or isinstance(file, str):
        data = open_dataset(file)
    else:
        data = file
    return "clon_bnds" in data.keys()


# Make sure that clon_bnds exists afterwards
def add_grid_information(nc_file, grid_file):
    grid_ds = psy.open_dataset(grid_file)
    if isinstance(nc_file, pathlib.PurePath) or isinstance(nc_file, str):
        icon_ds = psy.open_dataset(nc_file).squeeze()
    else:
        icon_ds = nc_file.squeeze()
    data = icon_ds.rename({"ncells": "cell"}).merge(grid_ds)
    for _k, v in six.iteritems(data.data_vars):
        add_cell_encoding(v)
    return data


def combine_grid_information(file, grid_file):

    if isinstance(grid_file, pathlib.PurePath) or isinstance(grid_file, str):
        grid = psy.open_dataset(grid_file)
    if isinstance(file, pathlib.PurePath) or isinstance(file, str):
        ds = open_dataset(file).squeeze()
    else:
        ds = file.squeeze()

    datasetType = xr.core.dataset.Dataset
    if type(ds) != datasetType or type(grid) != datasetType:
        raise Exception(
            """Grid or data file could not be opened to xr.core.dataset.Dataset."""
        )

    cell_dim = get_cell_dim_name(ds, grid)
    if "cell" not in ds.dims and cell_dim is not None:
        ds = ds.rename_dims({cell_dim: "cell"})

    edge_dim = get_edge_dim_name(ds, grid)
    if "edge" not in ds.dims and edge_dim is not None:
        ds = ds.rename_dims({edge_dim: "edge"})

    if cell_dim is None and edge_dim is None:
        raise WrongGridException(grid)

    time_coord = get_time_coord_name(ds)
    if time_coord != "time":
        ds = ds.rename(
            {"time": ds.coords["time"].attrs["standard_name"], time_coord: "time"}
        ).expand_dims("time")
    ds.time.attrs["axis"] = "T"

    if "cell" in ds.dims:
        ds = add_cell_data(ds, grid)
    if "edge" in ds.dims:
        ds = add_edge_data(ds, grid)

    for _k, v in six.iteritems(ds.data_vars):
        if "cell" in ds.data_vars[v.name].dims:
            add_cell_encoding(v)
        if "edge" in ds.data_vars[v.name].dims:
            add_edge_encoding(v)

    return ds


def get_cell_dim_name(ds, grid):
    cell_dim = None
    dims = [key for key in ds.dims]
    for dim in dims:
        dim_value = ds.dims[dim]
        if (
            dim_value == grid.dims["cell"]
        ):  # maybe this needs to be dynamic, if grid has ncells as cell dim name
            cell_dim = dim
    return cell_dim


def get_edge_dim_name(ds, grid):
    edge_dim = None
    dims = [key for key in ds.dims]
    for dim in dims:
        dim_value = ds.dims[dim]
        if (
            dim_value == grid.dims["edge"]
        ):  # maybe this needs to be dynamic, for example if grid has ncells as cell dim name, or edges vs edge
            edge_dim = dim
    return edge_dim


def get_time_coord_name(ds):
    try:
        if ds.coords["time"].attrs["standard_name"] != "time":
            coords = [key for key in ds.coords]
            for coord in coords:
                if "datetime" in str(ds.coords[coord].dtype):
                    if "standard_name" in ds.coords[coord].attrs:
                        if ds.coords[coord].attrs["standard_name"] == "time":
                            return coord
        else:
            return "time"
    except Exception:
        return "time"


def add_cell_data(ds, grid):
    ds = (
        ds.assign_coords(clon=("cell", np.float32(grid.coords["clon"].values)))
        .assign_coords(clat=("cell", np.float32(grid.coords["clat"].values)))
        .assign_coords(
            clat_bnds=(
                ("cell", "vertices"),
                np.float32(grid.coords["clat_vertices"].values),
            )
        )
        .assign_coords(
            clon_bnds=(
                ("cell", "vertices"),
                np.float32(grid.coords["clon_vertices"].values),
            )
        )
    )

    ds.clon.attrs["standard_name"] = "longitude"
    ds.clon.attrs["long_name"] = "cell longitude"
    ds.clon.attrs["units"] = "radian"
    ds.clon.attrs["bounds"] = "clon_bnds"
    ds.clat.attrs["standard_name"] = "latitude"
    ds.clat.attrs["long_name"] = "cell latitude"
    ds.clat.attrs["units"] = "radian"
    ds.clat.attrs["bounds"] = "clat_bnds"
    return ds


def add_edge_data(ds, grid):
    ds = (
        ds.assign_coords(elon=("edge", np.float32(grid.coords["elon"].values)))
        .assign_coords(elat=("edge", np.float32(grid.coords["elat"].values)))
        .assign_coords(
            elat_bnds=(("edge", "no"), np.float32(grid.coords["elat_vertices"].values))
        )
        .assign_coords(
            elon_bnds=(("edge", "no"), np.float32(grid.coords["elon_vertices"].values))
        )
        .assign_coords(zonal_normal_primal_edge=grid["zonal_normal_primal_edge"])
        .assign_coords(
            meridional_normal_primal_edge=grid["meridional_normal_primal_edge"]
        )
        .assign_coords(edge_system_orientation=grid["edge_system_orientation"])
    )

    ds.elon.attrs["standard_name"] = "longitude"
    ds.elon.attrs["long_name"] = "edge longitude"
    ds.elon.attrs["units"] = "radian"
    ds.elon.attrs["bounds"] = "elon_bnds"
    ds.elat.attrs["standard_name"] = "latitude"
    ds.elat.attrs["long_name"] = "edge latitude"
    ds.elat.attrs["units"] = "radian"
    ds.elat.attrs["bounds"] = "elat_bnds"

    clat_ind_access = lambda x: grid.coords["clat"][x - 1]
    clon_ind_access = lambda x: grid.coords["clon"][x - 1]

    ds.coords["elat_bnds"][:, 2] = ds.coords["elat_bnds"][:, 1]
    ds.coords["elat_bnds"][:, 1] = xr.apply_ufunc(
        clat_ind_access, grid["adjacent_cell_of_edge"][1, :]
    )
    ds.coords["elat_bnds"][:, 3] = xr.apply_ufunc(
        clat_ind_access, grid["adjacent_cell_of_edge"][0, :]
    )
    ds.coords["elon_bnds"][:, 2] = ds.coords["elon_bnds"][:, 1]
    ds.coords["elon_bnds"][:, 1] = xr.apply_ufunc(
        clon_ind_access, grid["adjacent_cell_of_edge"][1, :]
    )
    ds.coords["elon_bnds"][:, 3] = xr.apply_ufunc(
        clon_ind_access, grid["adjacent_cell_of_edge"][0, :]
    )

    normal_edge = xr.concat(
        [ds.zonal_normal_primal_edge, ds.meridional_normal_primal_edge], dim="cart"
    )
    normal_edge = normal_edge / np.linalg.norm(normal_edge, axis=0)
    ds = ds.assign_coords(
        zn=ds.zonal_normal_primal_edge
        / np.sqrt(
            ds.zonal_normal_primal_edge**2 + ds.meridional_normal_primal_edge**2
        )
    )
    ds = ds.assign_coords(
        mn=ds.meridional_normal_primal_edge
        / np.sqrt(
            ds.zonal_normal_primal_edge**2 + ds.meridional_normal_primal_edge**2
        )
    )
    ds = ds.assign_coords(normal_edge=normal_edge)

    return ds


def open_dataset(file):
    try:
        return psy.open_dataset(file)
    except Exception:
        try:
            return psy.open_dataset(
                file,
                engine="cfgrib",
                backend_kwargs={"indexpath": "", "errors": "ignore"},
            )
        except ValueError as e:
            if "conflicting sizes for dimension" in str(e):
                raise ValueError(
                    """It appears you have a heterogeneous GRIB file.
                Recommendation: Open the file using cfgrib.open_datasets() (returns an array of xr.Datasets)
                and pass in the relevent Dataset."""
                )
            else:
                raise ValueError(str(e))
        except Exception as e:
            raise Exception(str(e))
