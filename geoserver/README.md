geoserver
==========

install:
  1. install java 8
  1. grab geoserver -- https://docs.geoserver.org/latest/en/user/installation/index.html#installation
  1. wget https://build.geoserver.org/geoserver/2.14.x/geoserver-2.14.x-latest-bin.zip
  1. grab css plugin -- https://docs.geoserver.org/latest/en/user/styling/css/install.html
  1. wget https://build.geoserver.org/geoserver/2.14.x/ext-latest/geoserver-2.14-SNAPSHOT-css-plugin.zip
  1. cd geoserver/lib
  1. unzip ../g*css-plugin.zip 


osm tables:
  echo `psql -d osm -qAntc "select table_name from information_schema.tables where table_schema = 'osm';" | sort`

run:
  1. export DEV_DIR=/java/DEV # e.g., system specific
  1. cd $DEV_DIR/map_server 
  1. export GEOSERVER_DATA_DIR=$PWD/geoserver/data
  1. rm -rf $GEOSERVER_DATA_DIR
  1. git reset --hard HEAD
  1. bin/generate_geoserver_config
  1. cd <geoserver install directory>
  1. bin/startup.sh 
  1. cat $GEOSERVER_DATA_DIR/security/masterpw.info
  

Notes:
  1. ttf fonts: https://github.com/potyt/fonts
  1. may have to put fonts into JVM or System directories.
  1. https://gis.stackexchange.com/questions/30151/how-do-i-use-use-custom-fonts-for-labelling-in-geoserver