from ott.utils import gtfs_utils
from ott.utils import file_utils
from .templates.template import Template
from .base import get_data, make_layergroup, make_feature

import os
import logging
log = logging.getLogger(__file__)


def make_style_id(name, prefix='ott', suffix='style'):
    """ produces ott-routes-style """
    id = "{}-{}-{}".format(prefix, name, suffix)
    return id


def generate(data_dir="data_dir", workspace="ott"):
    """ 
    gen geoserver stuff
    """
    # lists for the layergroups.xml config
    routes_layers = []
    stops_layers = []
    workspace_path = os.path.join(data_dir, "workspaces", workspace)

    feed_list = gtfs_utils.get_feeds_from_config()
    for feed in feed_list:
        # step 1: get meta data and name for this feed
        schema_name = gtfs_utils.get_schema_name_from_feed(feed)
        data = get_data(schema=schema_name)

        # step 2: make datasource folder for each schema
        dir_path = os.path.join(workspace_path, schema_name)
        file_utils.mkdir(dir_path)

        # step 3: make the datastore config for the source
        ds_path = os.path.join(dir_path, 'datastore.xml')
        with open(ds_path, 'w+') as f:
            content = Template.data_store(data)
            f.write(content)

        # step 4: make stop and route feature layers
        routes_style_id = make_style_id('routes')
        stops_style_id = make_style_id('stops')
        r = make_feature(dir_path, data, 'routes', routes_style_id)
        s = make_feature(dir_path, data, 'stops',  stops_style_id)
        routes_layers.append(r)
        stops_layers.append(s)


    # step 5: make agency inclusive layergroups
    all_layers = []
    all_layers.extend(routes_layers)
    all_layers.extend(stops_layers)

    data['workspace'] = None
    make_layergroup(workspace_path, data, routes_layers, type_name='routes')
    make_layergroup(workspace_path, data, stops_layers, type_name='stops')
    make_layergroup(workspace_path, data, all_layers, type_name='routes_n_stops')


def generate_geoserver_config():
    """ generate geoserver config for transit """
    from ott.utils.parse.cmdline import osm_cmdline

    args = osm_cmdline.geoserver_parser()
    generate(args.data_dir)
