import datetime as dt


def get_lt(plotdate, simdate):
    """Get leadtime from a plotdate dt object
    Args:
        pltdt (dt): plottime
    Returns:
        str: lt [h]
    """
    # simdate = dt.datetime(2019,9,12,12,00)
    ltdt = plotdate-simdate
    ltdt_hf = ltdt.seconds/60/60 # hour fraction
    lt= ltdt.days*24+ltdt_hf

    return lt

# stolen from plot profile 
def lfff_name(lt):
    """Create mch-filename for icon ctrl run for given leadtime.
    Args:
        lt (int): leadtime
    Returns:
        str: filename of icon output simulation in netcdf, following mch-convention
    """
    hour = int(lt) % 24
    day = (int(lt) - hour) // 24
    remaining_s = round((lt - int(lt)) * 3600)
    sec = int(remaining_s % 60)
    mm = int((remaining_s - sec) / 60)

    return f"lfff{day:02}{hour:02}{mm:02}{sec:02}.nc"