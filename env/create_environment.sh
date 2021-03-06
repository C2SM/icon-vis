#!/bin/bash

PROJECT_FOLDER=/project/g110/pyvis
rm -rf ${PROJECT_FOLDER}
mkdir -p ${PROJECT_FOLDER}

# load python3
if [[ $slave == 'daint' ]]; then
	module load daint-gpu cray-python
elif [[ $slave == 'tsa' ]]; then
	module load python/3.7.4
fi

if [[ $slave == 'daint' ]]; then
	export EASYBUILD_PREFIX=${PROJECT_FOLDER}
	module load EasyBuild-custom
	eb GEOS-3.10.2-CrayGNU-21.09-python3.eb -r
	eb Eigen-3.4.0-CrayGNU-21.09.eb -r
   	module load GEOS Eigen PROJ Boost GSL
elif [[ $slave == 'tsa' ]]; then
	module use /apps/common/UES/sandbox/kraushm/tsa-PROJ/modules/all
	module load PrgEnv-gnu
	module load proj/8.0.0-fosscuda-2019b
	module load geos
	module load boost gsl cmake/3.14.5
fi

VENV_PATH=${PROJECT_FOLDER}/venv_${slave}

rm -rf $VENV_PATH
mkdir -p ${VENV_PATH}

python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

pip install --upgrade pip
pip install -r env/requirements.txt

if [[ $slave == 'daint' ]]; then
    pip install git+https://github.com/psyplot/psy-transect
fi
