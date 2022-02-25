import numpy as np
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
        np.sqrt((lats[i] - lat)**2 + (lons[i] - lon)**2)
        for i in range(len(lats))
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
