DIR=`dirname $0`
#. $DIR/base.sh

GS_DATA_DIR="data_dir"
DATA_PATH="$DIR/../$GS_DATA_DIR"
DATA_REPO="geoserver_data_dir"
DATA_REPO_URL="https://github.com/OpenTransitTools/${DATA_REPO}.git"


# clone clean data dir
if [ ! -d "$DATA_PATH" ]; then
  mkdir -p "$DATA_PATH"
  cd "$DATA_PATH"

  cmd="git init; git remote add origin $DATA_REPO_URL"
  echo $cmd
  eval $cmd 2> /dev/null
  sleep 2

  cmd="git config core.sparseCheckout true"
  echo $cmd 2> /dev/null
  sleep 2

  echo "$PWD/ >> .git/info/sparse-checkout"
  echo "$PWD/" >> .git/info/sparse-checkout
  sleep 2

  cmd="git pull origin main"
  echo $cmd
  eval $cmd
else
  cd "$DATA_PATH"
  git pull
fi

cd -

