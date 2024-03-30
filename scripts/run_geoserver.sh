if [ ! -d geoserver_data_dir ]; then
  echo "grab empty data_dir"
  scripts/download_clean_data_dir.sh
fi

if [ -d geoserver ]; then
  echo "using existing ./geoserver"
else
  echo "grab new geoserver"
  scripts/install_geoserver.sh
fi


read -n 1 -p "edit web port in .ini file, then CORS in webapps/geoserver/WEB-INF/web.xml (N to ignore): " edit
if [ "$edit" != "N" ]; then
  emacs geoserver/start.ini
  emacs geoserver/webapps/geoserver/WEB-INF/web.xml
fi

rm -rf data_dir geoserver/data_dir
cp -r geoserver_data_dir/data_dir .
bin/generate_geoserver_config -db localhost
mv data_dir geoserver/
cd geoserver
rm nohup.out
bin/shutdown.sh > /dev/null 2>&1
sleep 2
nohup bin/startup.sh &
