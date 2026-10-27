VER=3.0

EXT_PLUGINS="css-plugin vectortiles-plugin mbstyle-plugin"
COM_PLUGINS="gwc-mbtiles-plugin"

if [ -d "geoserverX" ]
then
    rm -rf geoserver-old
    mv geoserver geoserver-old
fi

if [ ! -f "geoserver.zip" ]
then
    if [ ! -d "geoserver" ]
    then
      geo="https://build.geoserver.org/geoserver/$VER.x/geoserver-$VER.x-latest-bin.zip"
      echo $geo
      curl $geo > geoserver.zip
    fi

    # see: https://build.geoserver.org/geoserver/master/ext-latest/
    for p in $EXT_PLUGINS
    do
        pl="https://build.geoserver.org/geoserver/$VER.x/ext-latest/geoserver-$VER.0-SNAPSHOT-$p.zip"
	echo $pl
	curl $pl > ${p}.zip
    done

    # see: https://build.geoserver.org/geoserver/master/community-latest/
    for p in $COM_PLUGINS
    do
        pl="https://build.geoserver.org/geoserver/$VER.x/community-latest/geoserver-$VER.0-SNAPSHOT-$p.zip"
	echo $pl
	curl $pl > ${p}.zip
    done
fi

mkdir geoserver
unzip geoserver.zip -d ./geoserver/ > /dev/null 
rm geoserver.zip

for p in $EXT_PLUGINS $COM_PLUGINS
do
  unzip -o ${p}.zip -d ./geoserver/webapps/geoserver/WEB-INF/lib/
  #rm ${p}.zip
done

cd geoserver
rm -rf data
rm -rf data_dir
ln -s ../data_dir .

# if map previews do not render (and you get sun.java2d.SurfaceData exceptions)
# see: https://gis.stackexchange.com/questions/402613/layer-preview-not-working-at-all-on-geoserver
rm -f webapps/geoserver/WEB-INF/lib/marlin-0.9.3.jar

# need ASM for .css plugin

ASM_VER=9.7
for x in asm asm-tree asm-analysis asm-util
do
  jar="webapps/geoserver/WEB-INF/lib/${x}.jar"
  curl https://repo1.maven.org/maven2/org/ow2/asm/asm/${ASM_VER}/asm-${ASM_VER}.jar > ${jar}
  ls -s $jar
done

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
