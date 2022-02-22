import psyplot.project as psy
import six


def add_encoding(obj):
    obj.encoding['coordinates'] = 'clat clon'


def check_grid_information(nc_file):
    data = psy.open_dataset(nc_file)
    return ('clon_bnds' in data.keys())


def add_grid_information(nc_file, grid_file):
    grid_ds = psy.open_dataset(grid_file)
    icon_ds = psy.open_dataset(nc_file).squeeze()
    data = icon_ds.rename({'ncells': 'cell'}).merge(grid_ds)
    for k, v in six.iteritems(data.data_vars):
        add_encoding(v)
    return data
