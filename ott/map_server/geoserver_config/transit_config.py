from ott.utils import gtfs_utils
from ott.utils import file_utils
from .templates.template import Template
from .base import get_data, make_layergroup, make_feature

import inspect
import os
import logging
log = logging.getLogger(__file__)


def make_style_id(name, prefix='ott', suffix='style'):
    """ produces ott-routes-style """
    id = "{}-{}-{}".format(prefix, name, suffix)
    return id


def make_workspace(data, workspace_path, schema_name):
    # step 1: make datasource folder for each schema
    dir_path = os.path.join(workspace_path, schema_name)
    file_utils.mkdir(dir_path)

    # step 2: make the datastore config for the source
    ds_path = os.path.join(dir_path, 'datastore.xml')
    with open(ds_path, 'w+') as f:
        content = Template.data_store(data)
        f.write(content)

    # step 3: return the directory path to then write layers to this workspace
    return dir_path


def make_current_config(data, workspace_path, schema_name='current'):
    dir_path = make_workspace(data, workspace_path, schema_name)

    # step w: make patterns layer (this view is K's (+30k) in size, so more for data geom for vehicles, ala
    #         geoserver/wfs?request=GetFeature&typeName=ott:patterns&outputFormat=json&cql_filter=route_id=1
    line_style_id = make_style_id('line')
    p = make_feature(dir_path, data, 'patterns', line_style_id)

    # step x: make route layer
    routes_style_id = make_style_id('routes')
    r = make_feature(dir_path, data, 'routes', routes_style_id)

    # step w: make rail layer
    rail_style_id = make_style_id('rail')
    t = make_feature(dir_path, data, 'rail', rail_style_id)

    # step y: make stop layer
    stops_style_id = make_style_id('stops')
    s = make_feature(dir_path, data, 'stops',  stops_style_id)

    # step z: make flex layer
    flex_style_id = make_style_id('flex')
    f = make_feature(dir_path, data, 'flex',  flex_style_id)

    make_layergroup(workspace_path, data, [f, t, r, s], schema_name)

    return p, r, t, s, f


def generate(args):
    """ 
    gen geoserver layers for gtfsdb
    layers:
     - individual layer groups based on each gtfs feed (eg., trimet, ctran, sam, rideconnection, etc...)
     - current schema rollup
    """
    routes_layers = []  # _layers will store the layers for the layergroups.xml config
    stops_layers = []

    workspace_path = os.path.join(args.data_dir, "workspaces", args.workspace)

    # current schema layers
    data = get_data(schema='current', **vars(args))
    make_current_config(data, workspace_path)

    # agency layer schema layers
    feed_list = gtfs_utils.get_feeds_from_config()
    for feed in feed_list:
        # step 1: get meta data and name for this feed / workspace
        schema_name = gtfs_utils.get_schema_name_from_feed(feed)
        data = get_data(schema=schema_name, **vars(args))
        dir_path = make_workspace(data, workspace_path, schema_name)

        # step 2: make route layer
        routes_style_id = make_style_id('routes')
        r = make_feature(dir_path, data, 'routes', routes_style_id)

        # step 3: make stop layer
        stops_style_id = make_style_id('stops')
        s = make_feature(dir_path, data, 'stops',  stops_style_id)

        routes_layers.append(r)
        stops_layers.append(s)

    # make inclusive layergroups
    all_layers = []
    all_layers.extend(routes_layers)
    all_layers.extend(stops_layers)


    data['workspace'] = None
    make_layergroup(workspace_path, data, all_layers, type_name='raw')


def generate_geoserver_config():
    """
    defacto main statment to generate geoserver data_dir based on config/app.ini 
    @see generate method above for specifics of what GS layers are being generated
    """
    from ott.utils.parse.cmdline import osm_cmdline
    from ott.utils import config_util

    params = ['db_user', 'db_pass', 'db_name', 'db_port', 'db_geoserver']
    def_params = config_util.get_params_from_config(params)

    def_params['workspace'] = def_params.get('db_user')   or 'ott'
    def_params['db_url'] = def_params.get('db_geoserver') or 'localhost'
    def_params['dir'] = "data_dir"

    #import pdb; pdb.set_trace()
    args = osm_cmdline.geoserver_parser(def_params)
    generate(args)


def get_agency_list():
    feed_list = gtfs_utils.get_feeds_from_config()
    list = []
    for f in feed_list:
        s = gtfs_utils.get_schema_name_from_feed(f)
        list.append(s)

    print(list)
