import math
import numpy as np

## CLASS DEFINITIN ##
# 1) variable dictionary
class Variable_dictionary:
    def __init__(self, name, title, units, min, max, ticks, cmap):
        self.name = name
        self.title = title
        self.units = units
        self.min = min
        self.max = max
        self.ticks = ticks
        self.cmap=cmap
    # name in icon output
    name = 'NAME'
    # title in plot
    title = 'TITLE'
    # color bar extent
    min = 0,100
    max = 100
    ticks = 10
    # colormap plt
    cmap = 'binary'

####################################################################
##  SET DICTS ##
# 2D vars
# 2m T
T_2M = Variable_dictionary('T_2M','2 m temperature','[°K]', 270, 300, 5,'RdYlBu')

# 2m Q
qv_2m = Variable_dictionary('qv_2m','2 m specific humidity','[g/kg]', 0,0.016, 0.001, 'YlGnBu_r')

# 10m wind
wind_10m = Variable_dictionary('wind_10m','10 m wind speed and direction','[m/s]',0,20,2,'RdPu')

# htopo
HSURF = Variable_dictionary('HSURF','topography','[m asl]',0,4000,100,'terrain')

# 3D vars
# Temperature
T = Variable_dictionary('T', 'Temperature', '[°K]', 220, 270, 5, 'RdYlBu')

# Pressure
P = Variable_dictionary('P', 'Pressure', '[hPa]', 300, 1000, 50, 'RdYlBu')

# Wind
U = Variable_dictionary('U','Zonal wind speed','[m/s]',-20,20,2,'RdPu')
V = Variable_dictionary('V','Meridional wind speed','[m/s]',-20,20,2,'RdPu')
W = Variable_dictionary('W','Vertical wind speed','[m/s]',-5,5,1,'RdPu')
VEL = Variable_dictionary('VEL','Wind speed','[m/s]',0,41,1,'viridis')
DIR = Variable_dictionary('DIR','Wind direction','[°]',0,361,10,'viridis')

# Specific humidity
QV = Variable_dictionary('QV','specific humidity','[g/kg]', 0,0.016, 0.001, 'YlGnBu_r')

# calc vars
# Potential Temperature
TH = Variable_dictionary('TH', 'Potential Temperature', '[°K]', 270, 295, 5, 'RdYlBu')


# TKE
####################################################################
## CALC FUNCTIONS ##
def calculate_wind_vel_from_uv(u, v): # from pp
    """Calculate wind velocity from U, V components.

    Args:
        u (pd series) u wind component in m/s
        v (pd series) v wind component in m/s

    Returns:
        pd series: wind velocity in m/s

    """
    wind_vel = np.sqrt(u**2 + v**2)

    return wind_vel

def calculate_wind_dir_from_uv(u, v, modulo_180=False): # from pp
    """Calculate wind direction from U, V components.

    Args:
        u (pd series):     u wind component in m/s
        v (pd series):     v wind component in m/s
        modulo_180 (bool): if True, retruned angle will be between [-180,180]

    Returns:
        pd series: wind direction in °

    """
    
    # convert to wind direction coordinate, different from trig unit circle coords
    # if the wind directin is 360 then returns zero (by %360)
    # inspired from wind_uv_to_dir function in:
    # https://github.com/blaylockbk/Ute_WRF/blob/master/functions/wind_calcs.py

    wind_dir = (270 - np.rad2deg(np.arctan2(v, u))) % 360

    # if requested convert from [0,360] to [-180,180]
    if modulo_180 == True:
        wind_dir = (wind_dir + 180) % 360 - 180
        # wind_dir  = np.rad2deg(np.arctan2(v, u))

    return wind_dir

def calculate_potT(T, P):
    """Calculate potential temperature from T and P.

    Args:
        T (pd series):     temperature in K
        P (pd series):     pressure in hPa
        modulo_180 (bool): if True, retruned angle will be between [-180,180]

    Returns:
        pd series: wind direction in °

    """
    #defining parameters
    press_r = 1000                  #reference pressure (hPa)
    Rd = 287                        #specific gas constant for dry air (J/kg*K)
    cp = 1004                       #speific heat of dry air at constant pressure (J/kg*K)

    #compute potential temperature
    potT = T*(press_r/P)**(Rd/cp)

    return potT