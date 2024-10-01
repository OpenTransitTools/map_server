DIR=`dirname $0`
. $DIR/base.sh

rm -rf ${NEW_DATA_DIR}
$DIR/download_clean_data_dir.sh
bc=`find ${NEW_DATA_DIR} | wc -l`
cd $DIR/..
git pull > /dev/null 2>&1
./bin/get_agencies
./bin/generate_geoserver_config
cd -
ac=`find ${NEW_DATA_DIR} | wc -l`

if [ $ac -gt $bc ]; then
  echo "success: data_dir has config with $ac files (blank dd has $bc)"
else
  echo "fail: data_dir $bc v. $ac files"
fi
