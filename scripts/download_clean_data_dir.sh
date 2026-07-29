DIR=`dirname $0`
. $DIR/base.sh


echo
echo "MAKE CLEAN ${GS_DATA_DIR} in $PWD"
echo

# bkup any old data dir
if [ -d "${PWD}/${GS_DATA_DIR}" ]; then
  echo "backup ${PWD}/${GS_DATA_DIR}"
  rm -rf "${GS_DATA_DIR}_OLD"
  mv ${GS_DATA_DIR} "${GS_DATA_DIR}_OLD"
fi

GS_DDIR_REPO="${DIR}/../${GS_DATA_DIR}_REPO"
rm -rf $GS_DDIR_REPO

# clone clean data dir
mkdir -p "$GS_DDIR_REPO"
cd "$GS_DDIR_REPO"

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

cd -

# copy fresh data dir
cp -r ${GS_DDIR_REPO}/${GS_DATA_DIR} ./
