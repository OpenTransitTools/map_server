#
# look at the ~/shp/*.shp directories, and create geoserver layers
#

DIR=`dirname $0`
. $DIR/base.sh

SHP_DIR=${1:-"$HOME/shp"}
DEF_SCHEMA=${2:-"current"}


function shp_to_gs() {
  shp_files="$1"
  style_name_override="$2"

  shp_base_name=$(basename $SHP_DIR)

  for s in $shp_files
  do
    parent_dir=$(basename "$(dirname "$s")")     # 'trimet' - e.g., dir name containing the .shp file
    schema=$DEF_SCHEMA
    if [ $parent_dir != $shp_base_name ]; then
      schema=$parent_dir
    fi

    layer=${s%.shp}
    layer=${layer##*/}
    style_name=$layer
    if [ $style_name_override ]; then
      style_name=$style_name_override
    fi

    cmd="poetry run generate-geoserver-layer -s $schema -l $layer -st $style_name"
    echo $cmd
    eval $cmd
  done
}


shp_to_gs "$SHP_DIR/*.shp"
shp_to_gs "$SHP_DIR/*/*.shp"
