import numpy as np
import six
import xarray
from scipy import stats


def ind_from_latlon(lats, lons, lat, lon, verbose=False):
    """Find the nearest neighbouring index to given location.

    Args:
        lats (2d array):            Latitude grid
        lons (2d array):            Longitude grid
        lat (float):                Latitude of location
        lon (float):                Longitude of location
        verbose (bool, optional):   Print information. Defaults to False.

    Returns:
        int     Index of nearest grid point.
    """
    dist = [
        np.sqrt((lats[i] - lat) ** 2 + (lons[i] - lon) ** 2) for i in range(len(lats))
    ]
    ind = np.where(dist == np.min(dist))[0][0]
    if verbose:
        print(f"Closest ind: {ind}")
        print(f" Given lat: {lat:.3f} vs found lat: {lats[ind]:.3f}")
        print(f" Given lon: {lon:.3f} vs found lon: {lons[ind]:.3f}")
    return ind


def add_coordinates(lon, lat, lonmin, lonmax, latmin, latmax):
    llon = lonmax - lonmin
    llat = latmax - latmin
    pos_lon = (lon - lonmin) / llon
    pos_lat = (lat - latmin) / llat
    return pos_lon, pos_lat


def get_stats(varin1, varin2):
    varin1_mean = np.mean(varin1, axis=0)
    varin2_mean = np.mean(varin2, axis=0)
    varin_diff = varin2_mean - varin1_mean
    # compute p values
    pval = stats.ttest_ind(varin1, varin2, 0)[1]
    return varin1_mean, varin2_mean, varin_diff, pval


def wilks(pvals, alpha):
    pval_1d = pvals.ravel()
    pval_rank = np.sort(pval_1d)
    N = np.size(pvals)
    alpha_fdr = 2 * alpha
    for i in range(len(pval_rank)):
        j = i + 1
        if pval_rank[i] > (j / N) * alpha_fdr:
            break
    pfdr = pval_rank[i]
    return pfdr


# show_data_vars can be used in python scripts to find out which variable name psyplot will need to plot that variable.
# eg if GRIB_cfVarName is defined, cfgrib will set this as the variable name, as opposed to GRIB_shortName.
def show_data_vars(ds):
    if type(ds) is str:
        Exception(
            "Argument is not a Dataset. Please open the dataset via psy.open_dataset() and pass returned Dataset to this function."
        )
    elif type(ds) is xarray.core.dataset.Dataset:
        print(
            "{:<15} {:<32} {:<20} {:<20} {:<10}".format(
                "psyplot name", "long_name", "GRIB_cfVarName", "GRIB_shortName", "units"
            )
        )
        for _k, v in six.iteritems(ds.data_vars):
            i = ds.data_vars[v.name]
            try:
                long_name = (
                    (i.long_name[:28] + "..") if len(i.long_name) > 28 else i.long_name
                )
            except Exception:
                long_name = ""
            try:
                units = i.units
            except Exception:
                units = ""
            try:
                gribcfvarName = i.GRIB_cfVarName
            except Exception:
                gribcfvarName = ""
            try:
                gribshortName = i.GRIB_shortName
            except Exception:
                gribshortName = ""
            print(
                "{:<15} {:<32} {:<20} {:<20} {:<10}".format(
                    v.name, long_name, gribcfvarName, gribshortName, units
                )
            )
