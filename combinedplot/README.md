# Combined Plot

**Description:**

The combined plot notebook plots the `U`, `V` vectors from ICON over Switzerland, ontop of a scalar temperature field. Because the ICON data is at a very high resolution, fieldextra has been used via iconarray's [core/interpolate.py](https://github.com/C2SM/iconarray/blob/main/iconarray/core/interpolate.py) module, to interpolate the wind data to a regular grid before plotting. The scalar data remains on the original ICON grid. The two datasets are plotted on top of one another using psyplot's Interactive Array. DWD ICONtools could also be used for the `U`, `V` data interpolation. Follow the installation instruction in the main folder or activate your virtual environment before starting the jupyter notebook.

### Example plot

To create the example plot below, activate your conda environment or venv and start the combinedplot jupyter notebook.

<p align="center">
<img src=combined_plot.png width="550"/>
</p>
