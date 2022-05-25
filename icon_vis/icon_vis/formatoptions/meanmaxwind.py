import psyplot.project as psy
from psyplot.plotter import Formatoption


class MeanMaxWind(Formatoption):

    #: the default value for the formatoption
    default = False

    def update(self, value):
        # method to update the plot
        if value is True:
            abs_mean = ((self.data[0] ** 2 + self.data[1] ** 2) ** 0.5).mean().values
            abs_max = ((self.data[0] ** 2 + self.data[1] ** 2) ** 0.5).max().values
            self.windtext = self.ax.text(
                0.0,
                -0.15,
                "Mean: %1.1f, Max: %1.1f [%s]" % (abs_mean, abs_max, "m/s"),
                transform=self.ax.transAxes,
            )
        else:
            if hasattr(self, "windtext"):
                self.windtext.remove()
                del self.windtext


psy.plot.mapvector.plotter_cls.meanmax_wind = MeanMaxWind("meanmax_wind")
psy.plot.mapcombined.plotter_cls.meanmax_wind = MeanMaxWind("meanmax_wind")
