VER=2.24

EXT_PLUGINS="css-plugin vectortiles-plugin mbstyle-plugin"
COM_PLUGINS="gwc-mbtiles-plugin"

if [ -d "geoserver" ];
then
    rm -rf geoserver-old
    mv geoserver geoserver-old
fi

if [ ! -f "geoserver.zip" ];
then
    curl "https://build.geoserver.org/geoserver/$VER.x/geoserver-$VER.x-latest-bin.zip" > geoserver.zip

    # see: https://build.geoserver.org/geoserver/master/ext-latest/
    for p in $EXT_PLUGINS
    do
        curl "https://build.geoserver.org/geoserver/$VER.x/ext-latest/geoserver-$VER-SNAPSHOT-$p.zip" > ${p}.zip
    done

    # see: https://build.geoserver.org/geoserver/master/community-latest/
    for p in $COM_PLUGINS
    do
        curl "https://build.geoserver.org/geoserver/$VER.x/community-latest/geoserver-$VER-SNAPSHOT-$p.zip" > ${p}.zip
    done
fi

mkdir geoserver
unzip geoserver.zip -d ./geoserver/
rm geoserver.zip

for p in $EXT_PLUGINS $COM_PLUGINS
do
  unzip -o ${p}.zip -d ./geoserver/webapps/geoserver/WEB-INF/lib/
  rm ${p}.zip
done

rm -rf geoserver/data
rm -rf geoserver/data_dir

# if map previews do not render (and you get sun.java2d.SurfaceData exceptions)
# see: https://gis.stackexchange.com/questions/402613/layer-preview-not-working-at-all-on-geoserver
rm geoserver/webapps/geoserver/WEB-INF/lib/marlin-0.9.3.jar

echo
echo "**** DO THIS TO GET geoserver UP & RUNNING ****"
echo
echo bin/generate_geoserver_config -db localhost
echo
echo "bin/run.sh &"
echo "    OR"
echo "export GEOSERVER_DATA_DIR=$PWD/geoserver/data"
echo "cd geoserver"
echo "nohup bin/startup.sh > logs/run.out &"
echo
echo mbtile preview:
echo http://localhost:8080/geoserver/gwc/demo/routes_n_stops
echo 
echo "***********************************************"
echo
