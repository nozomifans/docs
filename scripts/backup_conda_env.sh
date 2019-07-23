today=`date +%Y%m%d%H%M%S`
filename=$CONDA_DEFAULT_ENV.$today.yml
conda env export | grep -v "^prefix: "> $filename
mv $filename ../env_yaml/
unset today
unset filename
