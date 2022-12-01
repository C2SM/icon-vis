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
# Altitude
ALT = Variable_dictionary('ALT', 'Altitude', '[m AMSL]', 200, 5000, 250, 'RdYlBu')

# Temperature
T = Variable_dictionary('T', 'Temperature', '[°K]', 270, 311, 1, 'YlOrRd') #levels for vertical
T_h = Variable_dictionary('T', 'Temperature', '[°K]', 270, 311, 1, 'YlOrRd') #levels for horizontal

# Pressure
P = Variable_dictionary('P', 'Pressure', '[hPa]', 300, 1000, 50, 'RdYlBu')

# Wind
U = Variable_dictionary('U','Zonal wind speed','[m/s]',-20,20,2,'RdPu')
V = Variable_dictionary('V','Meridional wind speed','[m/s]',-20,20,2,'RdPu')
W = Variable_dictionary('W','Vertical wind speed','[m/s]',-5,5,1,'RdPu')
VEL = Variable_dictionary('VEL','Wind speed','[m/s]',0,41,1,'viridis') #bac:RdPu
DIR = Variable_dictionary('DIR','Wind direction','[°]',0,361,10,'viridis')

# Humidity
QV = Variable_dictionary('QV','Specific Humidity','[kg/kg]', 0,0.016, 0.0005, 'YlGnBu')
RH = Variable_dictionary('RH','Relative Humidity','[%]', 0,101,5, 'Blues')

# calc vars
# Potential Temperature
TH = Variable_dictionary('TH', 'Potential Temperature', '[°K]', 270, 295, 5, 'YlOrRd')
TD = Variable_dictionary('TD', 'Dewpoint Temperature', '[°K]', 270, 295, 5, 'YlOrRd')


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


def calculate_tdew_from_rh(rh, T, temperature_metric="celsius", verbose=False):
    """Calculate dew point temperature from relative humidity and temperature.

    Args:
        rh (pd series):    air relative humidity in %
        T (pd series):     air temperature in °C
        temperature_metric (str, optional): Input temperature unit. Defaults to "celsius".

    Returns:
        pandas series: dew point temperature timeseries (in °C or K)

    """
    if verbose:
        print(
            "Calculating dew point temperature (dewp_temp) from relative humidity and temp."
        )

    if temperature_metric != "celsius":
        if verbose:
            print("Assuming input temperature unit is Kelvin for rh calculation.")
        T = T - 273  # K to °C

    # inspired from humidity.to.dewpoint in:
    # https://github.com/geanders/weathermetrics/blob/master/R/moisture_conversions.R
    Tdew = (rh / 100) ** (1 / 8) * (112 + (0.9 * T)) - 112 + (0.1 * T)  # in °C

    if temperature_metric != "celsius":
        Tdew = Tdew + 273  # °C to K

    return Tdew

def calculate_qv_from_tdew(Press, Tdew, verbose=False):
    """Calculate specific humidity from pressure and dew point temperature.

    Args:
        Press (pd series):   air pressure in hPa
        Tdew (pd series):    dew point temperature in °C

    Returns:
        pandas series: specific humidity series in kg/kg

    """
    if verbose:
        print("Calculating specific humidity (qv) from press and dewp_temp.")

    # after eq. 4.24 in Practical Meteorology from Stull
    # P in hPa, Td in °C and qv in kg/kg
    e = 6.112 * np.exp((17.67 * Tdew) / (Tdew + 243.5))
    qv = (0.622 * e) / (Press - (0.378 * e))

    return qv

def calculate_qv_from_rh(Press, rh, T, verbose=False):
    """Calculate specific humidity from pressure, relative humidity and temperature.

    Args:
        Press (pd series):   air pressure series in hPa
        rh    (pd series):   air relative humidity in %
        T     (pd series):   air temperature in K

    Returns:
        pandas series: specific humidity series in kg/kg

    """
    if verbose:
        print("Calculating specific humidity (qv) from press and relative humidity.")

    Tdew = calculate_tdew_from_rh(rh, T)

    qv = calculate_qv_from_tdew(Press, Tdew)

    return qv
