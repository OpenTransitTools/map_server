from ott.utils import file_utils
from ott.utils.parse.cmdline import osm_cmdline
from .templates.template import Template

import os
import logging
log = logging.getLogger(__file__)


def make_feature(base_dir, data, type_name, style_id):
    """
    make routes feature folder
    """
    # step 1: make feature dir
    feature_path = os.path.join(base_dir, type_name)
    file_utils.mkdir(feature_path)

    # step 2: content
    data['type'] = type_name
    data['style'] = style_id

    # step 3: add featuretype.xml for this feature
    data['featuretype_id'] = "{}-{}-{}-featuretype".format(data['db_name'], data['schema'], type_name)
    type_path = os.path.join(feature_path, 'featuretype.xml')
    with open(type_path, 'w+') as f:
        content = Template.feature_type(data)
        f.write(content)

    # step 4: add layer.xml for this feature
    data['layer_id'] = "{}-{}-{}-layer".format(data['db_name'], data['schema'], type_name)
    layer_path = os.path.join(feature_path, 'layer.xml')
    with open(layer_path, 'w+') as f:
        content = Template.layer(data)
        f.write(content)

    return {'layer_id': data['layer_id'], 'style_id': style_id}


def change_style_color(layer_style_list, frm="Color", to="Gray"):
    """ for layergroups, we have a layer/style paried list ... this routine will rename the style items """
    # import pdb; pdb.set_trace()
    for l in layer_style_list:
        s = l['style_id'].replace(frm, to, 1)
        l['style_id'] = s


def make_layergroup(base_dir, data, layers, type_name):
    """
    make layergroup
    """
    # step 1: make feature dir
    layergroup_path = os.path.join(base_dir, 'layergroups')
    file_utils.mkdir(layergroup_path)

    # step 2: content
    data['type'] = type_name
    data['layers'] = layers

    # step 3: add layer.xml for this feature
    xml_path = os.path.join(layergroup_path, type_name + '.xml')
    with open(xml_path, 'w+') as f:
        content = Template.layer_group(data)
        f.write(content)


def get_data(db_name='ott', schema='TRIMET', user='ott', is_LatLon=True, do_namepace=True):
    v = {
        'db_name': db_name,
        'schema': schema,
        'user':  user,
        'store_id': "{}-{}-datastore".format(db_name, schema),
        'minx': -123.1 if is_LatLon else -13703429.32,
        'maxx': -121.1 if is_LatLon else -13480790.34,
        'miny':   44.0 if is_LatLon else   5465442.18,
        'maxy':   47.0 if is_LatLon else   5942074.07,
        'epsg':   4326 if is_LatLon else 3857
    }
    if do_namepace:
        v['namespace'] = db_name.capitalize() + 'Namespace'
        v['workspace'] = db_name.capitalize() + 'Workspace'

    return v


def generate_geoserver_config():
    # step 1: args
    args = osm_cmdline.geoserver_parser()
    do_layergroup = not args.ignore_layergroups

    # step 2: layer gen
    from . import osm_config
    from . import style_config
    from . import transit_config
    style_config.generate(args.data_dir)
    transit_config.generate(args.data_dir, gen_layergroup=do_layergroup)
    osm_config.generate(args.data_dir, gen_layergroup=do_layergroup)

    # step 3: create a new layergroup with both map and transit routes
    if do_layergroup:
        # FYI: very important to get the details (layer group ids correct) below, else GS will throw exceptions
        d = get_data(is_LatLon=False, do_namepace=False)
        d['published_type'] = "layerGroup"
        l = [{'layer_id':'osm-map-layergroup'}, {'layer_id':'ott-routes-layergroup'}]
        make_layergroup(args.data_dir, d, l, 'transit-map')

        l = [{'layer_id':'osm-map-gray-layergroup'}, {'layer_id':'ott-routes-layergroup'}]
        make_layergroup(args.data_dir, d, l, 'transit-map-gray')
