from ott.utils import file_utils

import os
import logging
log = logging.getLogger(__file__)


def write_file(dir_path, file_name, content):
    path = os.path.join(dir_path, file_name)
    with open(path, 'w') as f:
        f.write(content)


def make_style_id(name, prefix='ott', suffix='style'):
    """ produces ott-routes-style """
    id = "{}-{}-{}".format(prefix, name, suffix)
    return id


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
