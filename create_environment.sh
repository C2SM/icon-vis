#!/bin/bash
# load python3
if [[ $slave == 'daint' ]]; then 
	module load daint-gpu cray-python
elif [[ $slave == 'tsa' ]]; then 
	module load python/3.7.4
fi


if [[ $slave == 'daint' ]]; then 
	export EASYBUILD_PREFIX=/project/g110/pyvis
	module load EasyBuild-custom
	eb GEOS-3.10.2-CrayGNU-21.09-python3.eb -r
	module load GEOS
	module load PROJ
elif [[ $slave == 'tsa' ]]; then 
	module use /apps/common/UES/sandbox/kraushm/tsa-PROJ/modules/all
	module load PrgEnv-gnu
	module load proj/8.0.0-fosscuda-2019b
	module load geos
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

pip3 install --install-option="--prefix=/apps/arolla/UES/jenkins/RH7.9/MCH-PE20.08-UP01/gnu/19.2/easybuild/modules/all/eccodes/2.13.0-fosscuda-2019b-python3" eccodes
pip3 install cfgrib