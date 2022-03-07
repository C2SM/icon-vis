import psyplot.project as psy
import six
import pathlib


def add_encoding(obj):
    obj.encoding['coordinates'] = 'clat clon'


def check_grid_information(nc_file):
    if isinstance(nc_file,pathlib.PurePath) or isinstance(nc_file,str):
        data = psy.open_dataset(nc_file)
    else:
        data = nc_file
    return ('clon_bnds' in data.keys())


# Make sure that clon_bnds exists afterwards
def add_grid_information(nc_file, grid_file):
    grid_ds = psy.open_dataset(grid_file)
    if isinstance(nc_file,pathlib.PurePath) or isinstance(nc_file,str):
        icon_ds = psy.open_dataset(nc_file).squeeze()
    else:
        icon_ds = nc_file.squeeze()
    data = icon_ds.rename({'ncells': 'cell'}).merge(grid_ds)
    for k, v in six.iteritems(data.data_vars):
        add_encoding(v)
    return data
