DIR=`dirname $0`
. $DIR/base.sh

git_branch=${1:-"main"}

# generate the data_dir in this specific place, so all config runs get into same data_dir
cd $DIR/..

# download new / clean data_dir
if [ ! -d "${GS_DATA_DIR}" ] || [ "$git_branch" != "NONE" ]; then
  echo "creating a new geoserver data dir named '${PWD}/${GS_DATA_DIR}'"
  $DIR/download_clean_data_dir.sh "$git_branch"
fi
bc=`find ${GS_DATA_DIR} | wc -l`

# informational (eg reflect agencies list from config, ala ~/app.ini)
poetry run get-agencies

# generate transit data config
poetry run generate-geoserver-config

# generate data_dir/workspace/aerails (Metro only) and aerails_rtp (Metro, Oregon, Clark Co) .. see ~/ortho/ dir
poetry run generate-geoserver-aerial-config -workspace aerials
poetry run generate-geoserver-aerial-config -workspace aerials_rtp

# generate additional gs layers based on .shp files
$DIR/shps_to_layers.sh

# more info ... tell us how many new files were created from above
ac=`find ${GS_DATA_DIR} | wc -l`
if [ $ac -gt $bc ]; then
  echo "success: data_dir has config with $ac files (blank dd has $bc)"
else
  echo "fail: data_dir $bc v. $ac files"
fi

ls ${GS_DATA_DIR}/workspaces

echo "result: '${PWD}/${GS_DATA_DIR}' "
