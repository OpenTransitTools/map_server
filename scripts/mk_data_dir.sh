DIR=`dirname $0`
. $DIR/base.sh
$DIR/download_clean_data_dir.sh
bin/get_agencies
bin/generate_geoserver_config
