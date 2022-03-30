from psyplot.plotter import Formatoption
import psyplot.project as psy

import cartopy.feature as cf


class Borders(Formatoption):
    """Draw borders on a map"""

    default = {'color': 'black', 'linewidth': 0.0}

    def validate(self, value):
        if type(value) is dict:
            return value
        else:
            return bool(value)

    def update(self, value):
        if type(value) is dict:
            self.borders = self.ax.add_feature(cf.BORDERS,
                                               color=value['color'],
                                               linewidth=value['linewidth'])
        elif value is True:
            self.borders = self.ax.add_feature(cf.BORDERS,
                                               color='black',
                                               linewidth=1.0)
        else:
            if hasattr(self, "borders"):
                self.borders.remove()
                del self.borders


psy.plot.mapplot.plotter_cls.borders = Borders("borders")
psy.plot.mapvector.plotter_cls.borders = Borders("borders")
psy.plot.mapcombined.plotter_cls.borders = Borders("borders")
