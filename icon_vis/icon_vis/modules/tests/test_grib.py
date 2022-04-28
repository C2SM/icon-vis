import cfgrib
import icon_vis.modules as iconvis  # import icon-vis self-written modules

f_vt_vn = "data/example_data/grib/vnvt00010000"  # ONLY VN, VT variables
f_alldata = "data/example_data/grib/lfff00010000_edgeplots"  # VN, VT AND cell center variables (P, T, U, V etc)
f_grid = "data/example_data/grids/icon_grid_0001_R19B08_mch.nc"  # GRID file


def open_file(data):
    dss = cfgrib.open_datasets(
        data,
        engine="cfgrib",
        backend_kwargs={
            "indexpath": "",
            "errors": "ignore",
            "read_keys": ["typeOfLevel", "gridType"],
            "filter_by_keys": {"typeOfLevel": "generalVerticalLayer"},
        },
        encode_cf=("time", "geography", "vertical"),
    )
    ds_cell = dss[0]
    ds_edge = dss[1]
    return ds_cell, ds_edge


def test_grid_edge():

    _ds_cell, ds_edge = open_file(f_alldata)

    ds_edgevars = iconvis.combine_grid_information(ds_edge, f_grid)

    assert list(ds_edgevars.data_vars) == [
        "VN",
        "VT",
    ], "ds_edgevars should only have two data variables, ['VN', 'VT']"
    assert (
        len(ds_edgevars.edge.values) == 1567452
    ), "ds_edgevars should have a dimension edge, with length 1567452."
    assert "edge" in list(
        ds_edgevars.VN.dims
    ), "ds_edgevars data variables should have a dimension edge"
    assert (
        sum(
            [
                1
                for coord in ["elon", "elat", "elon_bnds", "elat_bnds"]
                if coord in ds_edgevars.coords
            ]
        )
        == 4
    ), "ds_edgevars should have coordinates 'elon', 'elat', 'elon_bnds', 'elat_bnds'"


def test_grid_cell():

    ds_cell, _ds_edge = open_file(f_alldata)

    ds_cellvars = iconvis.combine_grid_information(ds_cell, f_grid)

    assert list(ds_cellvars.data_vars) == [
        "P",
        "T",
        "U",
        "V",
        "QV",
        "QC",
        "QI",
    ], "ds_cellvars should only have two data variables, ['P', 'T', 'U', 'V', 'QV', 'QC', 'QI']"
    assert (
        len(ds_cellvars.cell.values) == 1043968
    ), "ds_cellvars should have a dimension 'cell', with length 1043968."
    assert "cell" in list(
        ds_cellvars.P.dims
    ), "ds_cellvars data variables should have a dimension 'cell'"
    assert (
        sum(
            [
                1
                for coord in ["clon", "clat", "clon_bnds", "clat_bnds"]
                if coord in ds_cellvars.coords
            ]
        )
        == 4
    ), "ds_cellvars should have coordinates 'clon', 'clat', 'clon_bnds', 'clat_bnds'"
