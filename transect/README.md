# Transect
> Note that there is currently a compatibility issue between different psyplot packages: [ModuleNotFoundError: No module named 'psyplot.compat' #62](https://github.com/psyplot/psyplot/issues/62)

This folder contains an example to plot transects on an ICON grid and was kindly provided by Philipp Sommer. It contains supplementary files to [O2A-Jourfix](https://github.com/Chilipp/psyplot-O2A-Jourfix-20210224), namely a demonstration of the [psy-transect package](https://github.com/psyplot/psy-transect) with an ICON file.

To create the example plot below, once you have already downloaded the example data, `cd transect` and run:

    python transect/plot_icon_transects.py

You will see two windows: The first one is a map with ICON output, the second one is the vertical profile. You can choose the transect to be plotted in Figure 2, by drawing a line with your mouse on Figure 1. At the same time you can change which altitude level is plotted on Figure 1 by changing the vertical transect line in Figure 2.  Note that the vertical profile is displayed with the original orography in meters using the 'HHL' variable.

<p float="center">
<img src=Figure_1_transect.png width="400"/>
<img src=Figure_2_transect.png width="400"/>
</p>
