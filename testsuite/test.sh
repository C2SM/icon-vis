#!/bin/bash

# This test script is used by the Jenkinsfile to run the iconarray tests with pytest.

source $WORKSPACE/miniconda_${NODE_NAME}/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}_${NODE_NAME}
python -m cfgrib selfcheck
python -c "import cartopy; print(cartopy.config)"

pytest testsuite/test*