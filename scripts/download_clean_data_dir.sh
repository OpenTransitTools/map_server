DIR=`dirname $0`
cd $DIR/../

# clone clean data dir
DATA_REPO="geoserver_data_dir"
DATA_REPO_URL="https://github.com/OpenTransitTools/${DATA_REPO}.git"
git clone $DATA_REPO_URL 2> /dev/null

# clean up existing space
rm -rf data_dir-ollddd
mv data_dir data_dir-ollddd 2> /dev/null
cp -r $DATA_REPO/data_dir .
