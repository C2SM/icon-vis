module load daint-gpu jupyter-utils
source load_env.sh
rm -rf $HOME/.local/share/jupyter/kernels/psyplot-kernel/
kernel-create -n psyplot-kernel
cd $HOME
ln -s $SCRATCH scratch
cd -
cp jupyter_launcher $HOME/.local/share/jupyter/kernels/psyplot-kernel/launcher
