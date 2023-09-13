from ott.utils import file_utils
from .style_config import make_id
from .templates.template import Template
from .base import get_data, make_layergroup, make_feature, change_style_color

import os
import logging
log = logging.getLogger(__file__)


def generate(data_dir="geoserver/data", workspace="osm/osm", gen_layergroup=True):
    """
    gen geoserver stuff
    :see: https://github.com/fegyi001/osmgwc#preview-the-layer-group
    """
    layer_group = []

    # step 1: make the datastore directory
    workspace_path = os.path.join(data_dir, "workspaces", workspace)
    file_utils.mkdir(workspace_path)

    # step 2: make the datastore config
    ds_path = os.path.join(workspace_path, 'datastore.xml')
    data = get_data('osm', 'osm', is_LatLon=False)
    with open(ds_path, 'w+') as f:
        content = Template.data_store(data)
        f.write(content)

    # step 3: make layers
    osm_layers = [
        "county",
        "country",
        "settlements",
        "district",
        "subdistrict",
        "boundary",

        "forestpark",
        "amenity",

        "water",
        "lakes",
        "waterway",

        "rails",
        "motorway",
        "pedestrian",
        "minor_roads",
        "roads",
        "trunk_primary",

        "buildings",
    ]
    for l in osm_layers:
        style_id = make_id(l, color="color")
        r = make_feature(workspace_path, data, l, style_id)
        layer_group.append(r)

    if gen_layergroup:
        data['workspace'] = None
        make_layergroup(data_dir, data, layer_group, type_name='map')

        # import pdb; pdb.set_trace()
        change_style_color(layer_group, "Color", "Gray")
        make_layergroup(data_dir, data, layer_group, type_name='map-gray')
