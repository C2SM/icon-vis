#!/bin/bash

# This test script is used by the Jenkinsfile to run the iconarray tests with pytest.

source $WORKSPACE/conda_${NODE_NAME}/etc/profile.d/conda.sh
source $WORKSPACE/conda_${NODE_NAME}/etc/profile.d/mamba.sh

conda activate ${CONDA_ENV_NAME}_${NODE_NAME}
export PYTHONNOUSERSITE=True
python -m cfgrib selfcheck
python -c "import cartopy; print(cartopy.config)"

pytest testsuite/test*.py
