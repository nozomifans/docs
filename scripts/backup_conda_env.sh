today=`date +%Y%m%d%H%M%S`
filename=$CONDA_DEFAULT_ENV.yml.$today
conda env export | grep -v "^prefix: "> $filename
mv $filename ../env_yaml/
unset today
unset filename
