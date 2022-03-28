# coding: utf-8
import psyplot.project as psy
import numpy as np
from psy_transect import utils
import matplotlib.pyplot as plt
from pathlib import Path


if __name__ == "__main__":

    data_dir = Path(Path(__file__).resolve().parents[1], 'data')
    icon_ds = psy.open_dataset(Path(data_dir, 'icon_19790101T000000Z.nc'))
    orography = psy.open_dataset(Path(data_dir,
                                      'icon_19790101T000000Zc.nc')).psy.HHL

    new_ds = utils.mesh_to_cf_bounds(orography, "height", "height_2", icon_ds)

    new_ds["clon"] = new_ds.clon.copy(data=np.rad2deg(new_ds.clon))
    new_ds["clat"] = new_ds.clat.copy(data=np.rad2deg(new_ds.clat))
    new_ds["clon"].attrs["units"] = "degrees_east"
    new_ds["clat"].attrs["units"] = "degrees_north"
    new_ds["clat_bnds"] = new_ds.clat_bnds.copy(data=np.rad2deg(new_ds.clat_bnds))
    new_ds["clon_bnds"] = new_ds.clon_bnds.copy(data=np.rad2deg(new_ds.clon_bnds))

    encodings = {v: var.encoding for v, var in new_ds.variables.items()}
    attrs = {v: var.attrs for v, var in new_ds.variables.items()}
    new_ds = new_ds.where(new_ds.HHL.notnull().any("height_2"), drop=True)
    for v, enc in encodings.items():
        new_ds[v].encoding.update(enc)

    for v, att in attrs.items():
        new_ds[v].attrs.update(att)
    new_ds.psy.plot.horizontal_maptransect(name="temp",
                                           transect=1000,
                                           cmap="Reds",
                                           decoder={"z": {"HHL"}})

    sp = new_ds.psy.plot.vertical_maptransect(
        name="temp",
        background="0.5",
        # datagrid="k-",
        transect_resolution=0.1,
        decoder={"z": {"HHL"}},
        ylim=(0, 6000),
        yticks=np.linspace(0, 6000, 7),
    )

    ax = sp.plotters[0].ax
    ax.set_ylim(0, 6000)
    ax.set_yticks(np.linspace(0, 6000, 7))
    sp.draw()

    p1, p2 = psy.gcp(True).plotters[-2:]
    p1.connect_ax(p2.ax)
    p2.connect_ax(p1.ax)

    plt.show()
