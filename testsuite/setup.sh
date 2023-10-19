#!/bin/bash

# This setup script is used by the Jenkinsfile to setup minimamba and create a mamba environment.

wget -O ${WORKSPACE}/mambaforge.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash mambaforge.sh -b -p $WORKSPACE/conda_${NODE_NAME}
source $WORKSPACE/conda_${NODE_NAME}/etc/profile.d/conda.sh
source $WORKSPACE/conda_${NODE_NAME}/etc/profile.d/mamba.sh


mamba config --set always_yes yes --set changeps1 no
mamba config --add channels conda-forge
mamba env create --name ${CONDA_ENV_NAME}_${NODE_NAME} --file env/environment.yml

mamba activate ${CONDA_ENV_NAME}_${NODE_NAME}
source env/setup-conda-env.sh

mamba deactivate
rm mambaforge.sh
