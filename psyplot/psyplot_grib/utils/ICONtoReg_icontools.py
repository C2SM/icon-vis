from pathlib import Path
import subprocess


init_fields_snippet = """
!
&input_field_nml
 inputname      = "{field}"         
 outputname     = "{field}"          
 intp_method    = 3
 loptional      = .FALSE.
 init_val       = 0.0
/
"""

init_remap_snippet = """
&remap_nml
 in_grid_filename  = '{grid_file}'
 in_filename       = '{data_file}'
 in_type           = 2
 out_filename      = '{file_out}'
 out_type          = 1
 out_filetype      = 4
 lsynthetic_grid   = .TRUE.  ! Specification of regular grids created from scratch (”synthetic regular grids”).
 corner1           = 5.5, 45.5
 corner2           = 11., 48.
 nxpoints          = 100
 nypoints          = 100
 l_have3dbuffer    = .false.
 !ncstorage_file    = "tmp/ncstorage_init.tmp"
/
"""

init_fields = [
    "U", "T", "V"
]

filetypes = {"grib2": (2, ""), "netcdf2": (4, ".nc"), "netcdf4": (5, ".nc")}

init_fields_namelist = "NAMELIST_ICONREMAP_FIELDS_INIT"
init_remap_namelist = "NAMELIST_ICONREMAP_INIT"

output_dir=Path('./tmp/icontools')
output_dir.mkdir(parents=True, exist_ok=True)

iconremap_cmd = "iconremap -q --remap_nml {} --input_field_nml {}"

def create_init_fields_namelist():
    with open(output_dir / Path(init_fields_namelist), "w") as f:
        for field in init_fields:
            f.write(init_fields_snippet.format(field=field))


def create_init_remap_namelist(data_file, grid_file, file_out, init_type):
    with open(output_dir / Path(init_remap_namelist), "w") as f:
        f.write(
            init_remap_snippet.format(
                data_file=data_file,
                grid_file=grid_file,
                file_out=file_out.resolve(),
                init_type=filetypes[init_type][0],
            )
        )

def create_remap_namelists(data_file, grid_file, file_out, init_type):
    create_init_fields_namelist()
    create_init_remap_namelist(data_file, grid_file, file_out, init_type)

def remap_ICON_to_Regulargrid(data_file, grid_file, init_type):
    file_out = output_dir/(Path(data_file).stem + "_regulargrid.nc")
    create_remap_namelists(data_file, grid_file, file_out, init_type)
    f = open("tmp/icontools/LOG.txt", "w")
    subprocess.run(["iconremap",  \
                "--remap_nml=tmp/icontools/NAMELIST_ICONREMAP_INIT",  \
                "--input_field_nml=tmp/icontools/NAMELIST_ICONREMAP_FIELDS_INIT" ], \
               stdout=f )
    return file_out.resolve()