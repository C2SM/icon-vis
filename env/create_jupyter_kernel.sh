module load daint-gpu jupyter-utils
source load_env.sh
rm -rf $HOME/.local/share/jupyter/kernels/psyplot-kernel/
kernel-create -n psyplot-kernel
# Link scratch (gives error if already linked)
cd $HOME
ln -s $SCRATCH scratch
cd -
touch $HOME/.jupyterhub.env
grep -qxF "export EASYBUILD_PREFIX=/project/g110/pyvis" $HOME/.jupyterhub.env || echo export EASYBUILD_PREFIX=/project/g110/pyvis >> $HOME/.jupyterhub.env
grep -qxF "module load daint-gpu EasyBuild-custom PROJ GEOS cray-python" $HOME/.jupyterhub.env || echo module load daint-gpu EasyBuild-custom PROJ GEOS cray-python >> $HOME/.jupyterhub.env
