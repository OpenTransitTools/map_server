from ott.utils import file_utils
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


def get_data(db_name='ott', db_port='5432', db_url='localhost', schema='TRIMET', db_user='ott', db_pass=None, is_LatLon=True, do_namepace=True, **kwargs):
    # TODO: bbox below should come from config ... but needs to be really big (larger than map in loader config) for cache to work / render lines 
    v = {
        'db_name': db_name,
        'db_port': db_port,
        'db_url': db_url,
        'schema': schema,
        'user':  db_user,
        'password':  db_pass,
        'store_id': "{}-{}-datastore".format(db_name, schema),
        'minx': -124.1 if is_LatLon else -13703429.32,
        'maxx': -120.1 if is_LatLon else -13480790.34,
        'miny':   41.0 if is_LatLon else   5465442.18,
        'maxy':   49.0 if is_LatLon else   5942074.07,
        'epsg':   4326 if is_LatLon else 3857
    }
    if do_namepace:
        v['namespace'] = db_name + '-namespace'
        v['workspace'] = db_name + '-workspace'

    return v
