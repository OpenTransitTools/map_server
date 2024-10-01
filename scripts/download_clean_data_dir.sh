DIR=`dirname $0`
. $DIR/base.sh

# clone clean data dir
if [ ! -d $DATA_REPO_DIR ]; then
  cmd="git clone $DATA_REPO_URL $DATA_REPO_DIR"
  echo $cmd
  eval $cmd 2> /dev/null
else
  cd $DATA_REPO_DIR
  git pull
  cd -
fi

# clean up existing space
rm -rf $NEW_DATA_DIR
cp -r $DATA_REPO_DIR/data_dir $NEW_DATA_DIR
