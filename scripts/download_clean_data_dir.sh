DIR=`dirname $0`
. $DIR/base.sh

# clone clean data dir
if [ ! -d $DATA_REPO_DIR ]; then
  cmd="git clone $DATA_REPO_URL $DATA_REPO_DIR"
  echo $cmd
  eval $cmd 2> /dev/null
fi

# clean up existing space
rm -rf data_dir-ollddd
mv data_dir data_dir-ollddd 2> /dev/null
cp -r $DATA_REPO_DIR/data_dir .
