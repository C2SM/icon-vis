import icon_vis.modules as iconvis  # import icon-vis self-written modules
import pytest
from icon_vis.modules import grid

f_wo_celldata = "data/example_data/nc/lfff01000000.nc"
f_w_celldata = "data/example_data/nc/lfff00000000z"
f_celldata_incomatible_w_grid = (
    "data/example_data/nc/my_exp1_atm_3d_ml_20180921T000000Z.nc"
)
f_grid = "data/example_data/grids/ICON-1E_DOM01.nc"


def test_wo_celldata():

    ds_cell = iconvis.combine_grid_information(f_wo_celldata, f_grid)

    assert "cell" in list(
        ds_cell.T.dims
    ), "ds_cell data variables should have a dimension 'cell'"
    assert (
        len(ds_cell.T.cell) == 1028172
    ), "ds_cell should have a dimension 'cell', with length 1028172."
    assert (
        sum(
            [
                1
                for coord in ["clon", "clat", "clon_bnds", "clat_bnds"]
                if coord in ds_cell.coords
            ]
        )
        == 4
    ), "ds_cell should have coordinates 'clon', 'clat', 'clon_bnds', 'clat_bnds'"


def test_w_celldata():

    ds_cell = iconvis.combine_grid_information(f_w_celldata, f_grid)

    assert "cell" in list(
        ds_cell.T.dims
    ), "ds_cell data variables should have a dimension 'cell'"
    assert (
        len(ds_cell.T.cell) == 1028172
    ), "ds_cell should have a dimension 'cell', with length 1028172."
    assert (
        sum(
            [
                1
                for coord in ["clon", "clat", "clon_bnds", "clat_bnds"]
                if coord in ds_cell.coords
            ]
        )
        == 4
    ), "ds_cell should have coordinates 'clon', 'clat', 'clon_bnds', 'clat_bnds'"


def test_wrong_grid():

    with pytest.raises(grid.WrongGridException):
        iconvis.combine_grid_information(f_celldata_incomatible_w_grid, f_grid)
