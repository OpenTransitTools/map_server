DIR=`dirname $0`
. $DIR/base.sh

echo "creating a new geoserver data-dir named '${GS_DATA_DIR}'"
$DIR/download_clean_data_dir.sh aerials
bc=`find ${GS_DATA_DIR} | wc -l`
cd $DIR/..
git pull > /dev/null 2>&1
# generate data_dir/workspace/aerails (Metro only) and aerails_rtp (Metro, Oregon, Clark Co) .. see ~/ortho/ dir
poetry run generate-geoserver-aerial-config -workspace aerials
poetry run generate-geoserver-aerial-config -workspace aerials_rtp
cd -
ac=`find ${GS_DATA_DIR} | wc -l`

if [ $ac -gt $bc ]; then
  echo "success: data_dir has config with $ac files (blank dd has $bc)"
else
  echo "fail: data_dir $bc v. $ac files"
fi

ls ${GS_DATA_DIR}/workspaces
