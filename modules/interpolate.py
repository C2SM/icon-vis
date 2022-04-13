from pathlib import Path
import subprocess
from subprocess import PIPE, STDOUT
import os

# ----------------------------------------------------------------------
#
# functions and definitions for ICON grid A to ICON grid B interpolation
# via fieldextra
#
# ----------------------------------------------------------------------

icon_icon_remap_namelist = """
!*********************************************************************************************
! Namelist for remapping ICON grid to low resolution R19B04 ICON grid.
! Usage: fieldextra remap.nl
!        where fieldextra points to /project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp
!*********************************************************************************************
!!!! HEADER
! Global settings
&RunSpecification
 verbosity             = "high"
 additional_diagnostic = .true.
 n_ompthread_total = 6
/
&GlobalResource
 dictionary            = "/project/s83c/fieldextra/tsa/resources/dictionary_icon.txt"
 grib_definition_path  = "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_cosmo",
                         "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_vendor"
 grib2_sample          = "/project/s83c/fieldextra/tsa/resources/eccodes_samples/COSMO_GRIB2_default.tmpl"
 icon_grid_description = '{in_grid_file}',
                         '{out_grid_file}'
/
&GlobalSettings
 default_model_name            = "icon"
 default_product_category      = "determinist"
 default_out_type_stdlongitude = .true.
/
! Model specifc information
&ModelSpecification
 model_name            = "icon"
 regrid_method         = "icontools,rbf",
/
! Information associated to imported NetCDF file
&NetCDFImport
 dim_default_attribute = "ncells:long_name=unstructured_grid_cell_index value=index",
                         "alt: axis=z standard_name=height",
/
!!!! PRODUCT
&Process
  in_file='{data_file}'
  out_file='{file_out}', out_type="NETCDF",
  out_regrid_target = "icon_grid,cell,{out_grid_file}"
  out_regrid_method = "default"
  in_size_vdate = {num_dates}
  out_type_nccoordbnds = .true.
/
&Process in_field = "U" /
&Process in_field = "V" /
"""


def create_ICON_to_ICON_remap_namelist(remap_namelist_path, data_file,
                                       in_grid_file, out_grid_file, file_out,
                                       num_dates):

    with open(remap_namelist_path, "w") as f:
        f.write(
            icon_icon_remap_namelist.format(data_file=data_file,
                                            in_grid_file=in_grid_file,
                                            out_grid_file=out_grid_file,
                                            file_out=file_out.resolve(),
                                            num_dates=num_dates
                                            #init_type=filetypes[init_type][0],
                                            ))


def remap_ICON_to_ICON(data_file, in_grid_file, out_grid_file, num_dates):

    remap_namelist_fname = "NAMELIST_ICON_ICON_REMAP"
    output_dir = Path('./tmp/fieldextra')
    remap_namelist_path = output_dir / remap_namelist_fname
    file_out = output_dir / (Path(data_file).stem +
                             "_interpolated_ICON_grid.nc")
    data_file = os.path.abspath(data_file)
    in_grid_file = os.path.abspath(in_grid_file)
    out_grid_file = os.path.abspath(out_grid_file)
    # Path to fieldextra as defined by env/setup-conda-env.sh
    fieldextra_exe = os.environ['FIELDEXTRA_PATH']
    # LOG file
    f = open("tmp/fieldextra/LOG_ICON_LOWRES_REMAP.txt", "w")

    # Create tmp directory for results and namelist
    output_dir.mkdir(parents=True, exist_ok=True)

    filetypes = {
        "grib2": (2, ""),
        "netcdf2": (4, ".nc"),
        "netcdf4": (5, ".nc")
    }

    # Create namelist
    create_ICON_to_ICON_remap_namelist(remap_namelist_path, data_file,
                                       in_grid_file, out_grid_file, file_out,
                                       num_dates)

    # Run fieldextra with namelist
    subprocess.run([fieldextra_exe,  \
                    remap_namelist_path], \
                    stdout=f )

    return file_out.resolve()


# ----------------------------------------------------------------------
#
# functions and definitions for ICON grid A to Regular grid interpolation
# via fieldextra
#
# ----------------------------------------------------------------------

icon_reg_remap_namelist = """
!*********************************************************************************************
! Namelist for remapping ICON grid to regular grid
! Usage: fieldextra remap.nl
!        where fieldextra points to /project/s83c/fieldextra/tsa/bin/fieldextra_gnu_opt_omp
!*********************************************************************************************
!!!! HEADER
! Global settings
&RunSpecification
 verbosity             = "high"
 additional_diagnostic = .true.
 n_ompthread_total = 1
/
&GlobalResource
 dictionary            = "/project/s83c/fieldextra/tsa/resources/dictionary_icon.txt"
 grib_definition_path  = "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_cosmo",
                         "/project/s83c/fieldextra/tsa/resources/eccodes_definitions_vendor"
 grib2_sample          = "/project/s83c/fieldextra/tsa/resources/eccodes_samples/COSMO_GRIB2_default.tmpl"
 icon_grid_description = '{grid_file}'
/
&GlobalSettings
 default_model_name            = "icon"
 default_product_category      = "determinist"
 default_out_type_stdlongitude = .true.
/
! Model specifc information
&ModelSpecification
 model_name            = "icon"
 regrid_method         = "icontools,rbf",
/
! Information associated to imported NetCDF file
&NetCDFImport
 dim_default_attribute = "ncells:long_name=unstructured_grid_cell_index value=index",
                         "alt: axis=z standard_name=height",
 varname_translation   = "clon_bnds:__IGNORE__", "clat_bnds:__IGNORE__",
                         "clon:__IGNORE__", "clat:__IGNORE__",
/
!!!! PRODUCT
&Process
  in_file='{data_file}'
  out_file='{file_out}', out_type="NETCDF",
  out_regrid_target = '{out_regrid_target}'
  out_regrid_method = "default"
  in_size_vdate = {num_dates}
/
&Process in_field = "U" /
&Process in_field = "V" /
"""


def create_ICON_to_Regulargrid_remap_nl(remap_namelist_path, data_file,
                                        grid_file, file_out, num_dates, out_regrid_target):
    print('Creating Namelist')
    with open(remap_namelist_path, "w") as f:
        f.write(
            icon_reg_remap_namelist.format(data_file=data_file,
                                           grid_file=grid_file,
                                           file_out=file_out.resolve(),
                                           num_dates=num_dates,
                                           out_regrid_target=out_regrid_target,
                                           #init_type=filetypes[init_type][0],
                                           ))
    print('Finished Namelist')


def remap_ICON_to_regulargrid(data_file, grid_file, num_dates, region='Swizerland'):
    print('Remap ICON to regular grid')
    remap_namelist_fname = "NAMELIST_ICON_REG_REMAP"
    output_dir = Path('./tmp/fieldextra')
    remap_namelist_path = output_dir / remap_namelist_fname
    file_out = output_dir / (Path(data_file).stem +
                             "_interpolated_regulargrid.nc")
    data_file = os.path.abspath(data_file)
    grid_file = os.path.abspath(grid_file)
    print('data')
    print('data file: ' + str(data_file))
    # Path to fieldextra as defined by env/setup-conda-env.sh
    fieldextra_exe = os.environ['FIELDEXTRA_PATH']

    # Create tmp directory for results and namelist
    output_dir.mkdir(parents=True, exist_ok=True)

    filetypes = {
        "grib2": (2, ""),
        "netcdf2": (4, ".nc"),
        "netcdf4": (5, ".nc")
    }

    if str(region).lower() in ['swizerland', 'ch']:
        out_regrid_target = "geolatlon,5500000,45500000,11000000,48000000,55000,25000"
    elif str(region).lower() in 'europe':
        out_regrid_target = 'geolatlon,0,40000000,20000000,50000000,20000,10000'
    elif str(region) == 'custom latlon':
        out_regrid_target = "geolatlon,5500000,45500000,11000000,48000000,55000,25000"

    # Create namelist
    create_ICON_to_Regulargrid_remap_nl(remap_namelist_path, data_file,
                                        grid_file, file_out, num_dates, out_regrid_target)

    # LOG file
    with open(output_dir / "LOG_ICON_REG_REMAP.txt", "w") as f:

        # Run fieldextra with namelist
        fxcall = subprocess.Popen([fieldextra_exe,  \
                        remap_namelist_path], \
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = fxcall.communicate()

        f.write(out)
        f.write(err)
        f.close()

    return file_out.resolve()
