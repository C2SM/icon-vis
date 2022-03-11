#!/bin/bash
# load python3
if [[ $slave == 'daint' ]]; then 
	module load daint-gpu cray-python
else
	module load python/3.7.4
fi

export EASYBUILD_PREFIX=/project/g110/pyvis
module load EasyBuild-custom
eb GEOS-3.10.2-CrayGNU-21.09-python3.eb -r
module load GEOS

if [[ $slave == 'daint' ]]; then 
	module load PROJ
fi

# cf-grib engine 
if [[ $slave == 'tsa' ]]; then 
	source ~osm/.opr_setup_dir
	export PATH=$OPR_SETUP_DIR/bin:$PATH
	export MODULEPATH=$MODULEPATH\:$OPR_SETUP_DIR/modules/modulefiles
	
	module load PrgEnv-gnu/19.2
	module load eccodes/2.19.0-gnu-8.3.0-nocuda-noomp
	module load eccodes_cosmo_resources/2.19.0.5
fi

VENV_PATH=/project/g110/pyvis/venv_$slave

rm -rf $VENV_PATH
mkdir -p ${VENV_PATH}


python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
