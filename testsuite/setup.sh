#!/bin/bash

# This setup script is used by the Jenkinsfile to setup miniconda and create a conda environment.

wget -O ${WORKSPACE}/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash miniconda.sh -b -p $WORKSPACE/miniconda_${NODE_NAME}
source $WORKSPACE/miniconda_${NODE_NAME}/etc/profile.d/conda.sh

conda config --set always_yes yes --set changeps1 no
conda config --add channels conda-forge
conda config --set channel_priority strict
export PYTHONNOUSERSITE=True
conda env create --name ${CONDA_ENV_NAME}_${NODE_NAME} --file env/environment.yml

conda activate ${CONDA_ENV_NAME}_${NODE_NAME}
source env/setup-conda-env.sh

conda deactivate
rm miniconda.sh
