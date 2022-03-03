#!/bin/bash
# load python3
if [[ $slave == 'daint' ]]; then 
	module load cray-python
    module load daint-gpu
else:
	module load python/3.7.4

git clone https://github.com/eth-cscs/production.git
export EB_CUSTOM_REPOSITORY=production/easybuild

module EasyBuild-custom
eb GEOS-3.10.2-CrayGNU-21.09-python3.eb -r
eb PROJ-8.1.1-CrayGNU-21.09.eb -r
module load GEOS PROJ


VENV_PATH=/project/g110/pyvis/venv_$slave

rm -rf $VENV_PATH
mkdir -p ${VENV_PATH}


python3 -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
