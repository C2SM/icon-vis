module load daint-gpu jupyter-utils
source load_env.sh
rm -rf $HOME/.local/share/jupyter/kernels/psyplot-kernel/
kernel-create -n psyplot-kernel
sed -i '/activate/i export EASYBUILD_PREFIX=\/project\/g110\/pyvis\nmodule load daint-gpu EasyBuild-custom PROJ GEOS cray-python' $HOME/.local/share/jupyter/kernels/psyplot-kernel/launcher
# Link scratch (gives error if already linked)
cd $HOME
ln -s $SCRATCH scratch
cd -
