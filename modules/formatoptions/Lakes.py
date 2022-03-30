from psyplot.plotter import Formatoption
import psyplot.project as psy

from cartopy.feature import GSHHSFeature


class Lakes(Formatoption):

    #: the default value for the formatoption
    default = True

    def update(self, value):
        # method to update the plot
        if value is True:
            self.lakes = self.ax.add_feature(
                GSHHSFeature(scale='high',
                             levels=[2],
                             alpha=0.8,
                             linewidth=0.4))
        else:
            self.remove()

    def remove(self):
        if self.lakes is None:
            return
        self.lakes.remove()
        del self.lakes


psy.plot.mapplot.plotter_cls.lakes = Lakes("lakes")
