# Plotting Edge Variables

**Description:**

The edgeplot notebook uses GRIB data with psyplot to visualize VN, and VT - the normal and tangential components of wind calculated on the edge of the ICON grid cells, unlike the other variabled plotted in this repo which are on the cell center.
The absolute wind variable is derived from VN and VT, to form the scalar map plot.
The x and y (or lon/lat) components of wind on the cell edge is also derived, to create the vector plot. This is because psyplot expects vectors on the lon/lat orientation, instead of normal and tangential to the cell edge.

Follow the installation instruction in the main folder or activate your virtual environment before starting the jupyter notebook.

### Example plot 

To create the example plots below, activate your conda environment or venv and start the edgeplot jupyter notebook.
    
#### Edge Scalar Plot 
<p align="center">
<img src=edge_scalar_plots.png/>
</p>

    
#### Edge Vector Plot 
<p align="center">
<img src=vector_edge_plot.png width="550"/>
</p>
