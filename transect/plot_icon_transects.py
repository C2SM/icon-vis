# coding: utf-8
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import psyplot.project as psy
from psy_transect import utils
from ipdb import set_trace
if __name__ == "__main__":
    
    filename = 'lfff00000000.nc'
    nc_file = '/store/s83/swester/teamx/tdf_2019091212/output/19091212/'#+filename
    data_dir = nc_file
    icon_ds = psy.open_dataset(Path(data_dir, "lfff00000000.nc"))
    orography = psy.open_dataset(Path(data_dir, "lfff00000000c.nc")).psy.HHL

    new_ds = utils.mesh_to_cf_bounds(orography, "height", "height_3", icon_ds)

    new_ds["clon"] = new_ds.clon.copy(data=np.rad2deg(new_ds.clon))
    new_ds["clat"] = new_ds.clat.copy(data=np.rad2deg(new_ds.clat))
    new_ds["clon"].attrs["units"] = "degrees_east"
    new_ds["clat"].attrs["units"] = "degrees_north"
    new_ds["clat_bnds"] = new_ds.clat_bnds.copy(data=np.rad2deg(new_ds.clat_bnds))
    new_ds["clon_bnds"] = new_ds.clon_bnds.copy(data=np.rad2deg(new_ds.clon_bnds))

    encodings = {v: var.encoding for v, var in new_ds.variables.items()}
    attrs = {v: var.attrs for v, var in new_ds.variables.items()}
    new_ds = new_ds.where(new_ds.HHL.notnull().any("height_3"), drop=True)
    for v, enc in encodings.items():
        new_ds[v].encoding.update(enc)

    for v, att in attrs.items():
        new_ds[v].attrs.update(att)
    new_ds.psy.plot.horizontal_maptransect(
        name="T",
        transect=1000,
        cmap="Reds",
        decoder={"z": {"HHL"}},
        clabel="Temperature (K)",
    )

    sp = new_ds.psy.plot.vertical_maptransect(
        name="T",
        background="0.5",
        transect_resolution=0.1,
        decoder={"z": {"HHL"}},
        ylim=(0, 6000),
        yticks=np.linspace(0, 6000, 7),
        clabel="Temperature (K)",
    )

    ax = sp.plotters[0].ax
    ax.set_ylabel('Altitude [m asl]')
    ax.set_ylim(0, 6000)
    ax.set_yticks(np.linspace(0, 6000, 7))

    ax.set_xlabel('Distance [km]')
    sp.draw()

    # set_trace()
    p1, p2 = psy.gcp(True).plotters[-2:]
    p1.connect_ax(p2.ax)
    p2.connect_ax(p1.ax)

    plt.savefig('/users/tlezuo/icon-vis/transect/transect.png')
    plt.show()
