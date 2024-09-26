DIR=`dirname $0`
. $DIR/base.sh
git pull
$DIR/download_clean_data_dir.sh
bc=`find ${DIR}/../data_dir | wc -l`
bin/get_agencies
bin/generate_geoserver_config
ac=`find ${DIR}/../data_dir | wc -l`

if [ $ac -gt $bc ]; then
  echo "success: data_dir has config with $ac files (blank dd has $bc)"
else
  echo "fail: data_dir $bc v. $ac files"
fi
