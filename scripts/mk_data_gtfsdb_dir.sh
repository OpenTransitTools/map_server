DIR=`dirname $0`
. $DIR/base.sh

echo "creating a new geoserver data-dir named '${GS_DATA_DIR}'"
$DIR/download_clean_data_dir.sh
bc=`find ${GS_DATA_DIR} | wc -l`
cd $DIR/..
git pull > /dev/null 2>&1
poetry run get-agencies
poetry run generate-geoserver-config
cd -
ac=`find ${GS_DATA_DIR} | wc -l`

if [ $ac -gt $bc ]; then
  echo "success: data_dir has config with $ac files (blank dd has $bc)"
else
  echo "fail: data_dir $bc v. $ac files"
fi
