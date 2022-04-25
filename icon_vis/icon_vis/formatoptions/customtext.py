import psyplot.project as psy
from psyplot.plotter import Formatoption


class CustomText(Formatoption):

    #: the default value for the formatoption
    default = False

    def update(self, value):
        # method initialize the plot in the very beginning
        if type(value) is str:
            if hasattr(self, "text"):
                self.remove()
            self.text = self.ax.text(
                0.0,
                -0.15,
                value,
                fontsize="xx-large",
                # ha='right', va='top',   # text alignment,
                transform=self.ax.
                transAxes,  # coordinate system transformation)
            )
        elif value in [False, None] and hasattr(self, "text"):
            self.remove()

    def remove(self):
        if self.text is None:
            return
        self.text.remove()
        del self.text


psy.plot.mapplot.plotter_cls.customtext = CustomText("customtext")
psy.plot.mapvector.plotter_cls.customtext = CustomText("customtext")
psy.plot.mapcombined.plotter_cls.customtext = CustomText("customtext")
