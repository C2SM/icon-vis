# Load modules
import configparser
import sys


def get_several_input(config, sect, opt, f=False, i=False):
    var = config.get(sect, opt)
    var = var.replace(', ', ',')
    var = var.split(',')
    if f:
        var = list(map(float, var))
    if i:
        var = list(map(int, var))
    return var


def read_config(config_path):
    config = configparser.ConfigParser(inline_comment_prefixes='#')
    try:
        config.read(config_path)
    except Exception as e:
        sys.exit("Please provide a valid config file")

    # Read information regarding the variable
    var = {}
    if config.has_option('var', 'name'):
        var['name'] = config.get('var', 'name')
    else:
        sys.exit("No variable name given")
    if config.has_option('var', 'varlim'):
        var['varlim'] = get_several_input(config, 'var', 'varlim', f=True)
    if config.has_option('var', 'grid_file'):
        var['grid_file'] = config.get('var', 'grid_file')
    if config.has_option('var', 'time'):
        var['time'] = get_several_input(config, 'var', 'time', i=True)
    else:
        var['time'] = [0]
    if config.has_option('var', 'height'):
        var['height'] = get_several_input(config, 'var', 'height', i=True)
    else:
        var['height'] = [0]
    if config.has_option('var', 'unc'):
        var['unc'] = config.get('var', 'unc')

    # Read information regarding the map
    map = {}
    if config.has_option('map', 'lonmin'):
        map['lonmin'] = config.getfloat('map', 'lonmin')
    if config.has_option('map', 'lonmax'):
        map['lonmax'] = config.getfloat('map', 'lonmax')
    if config.has_option('map', 'latmin'):
        map['latmin'] = config.getfloat('map', 'latmin')
    if config.has_option('map', 'latmax'):
        map['latmax'] = config.getfloat('map', 'latmax')
    if config.has_option('map', 'add_grid'):
        map['add_grid'] = config.getboolean('map', 'add_grid')
    if config.has_option('map', 'projection'):
        map['projection'] = config.get('map', 'projection')
    if config.has_option('map', 'title'):
        map['title'] = config.get('map', 'title')

    # Read information regarding coordinates
    coord = {}
    if config.has_option('coord', 'name'):
        coord['name'] = get_several_input(config, 'coord', 'name')
    if config.has_option('coord', 'lon'):
        coord['lon'] = get_several_input(config, 'coord', 'lon', f=True)
    if config.has_option('coord', 'lat'):
        coord['lat'] = get_several_input(config, 'coord', 'lat', f=True)
    if config.has_option('coord', 'marker'):
        coord['marker'] = get_several_input(config, 'coord', 'marker')
    if config.has_option('coord', 'marker_size'):
        coord['marker_size'] = get_several_input(config,
                                                 'coord',
                                                 'marker_size',
                                                 f=True)
    if config.has_option('coord', 'col'):
        coord['col'] = get_several_input(config, 'coord', 'col')

    #Read information regarding plot
    plot = {}
    if config.has_option('plot', 'xlabel'):
        plot['xlabel'] = config.get('plot', 'xlabel')
    if config.has_option('plot', 'ylabel'):
        plot['ylabel'] = config.get('plot', 'ylabel')
    if config.has_option('plot', 'xlim'):
        plot['xlim'] = get_several_input(config, 'plot', 'xlim', f=True)
    if config.has_option('plot', 'ylim'):
        plot['ylim'] = get_several_input(config, 'plot', 'ylim', f=True)
    if config.has_option('plot', 'title'):
        plot['title'] = config.get('plot', 'title')
    if config.has_option('plot', 'date_format'):
        plot['date_format'] = config.get('plot', 'date_format')
    else:
        plot['date_format'] = '%Y-%m-%d %H:%M'

    return [var, map, coord, plot]
