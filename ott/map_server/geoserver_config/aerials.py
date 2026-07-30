import os
from pathlib import Path

from ott.utils import file_utils

from .templates.template import Template
from .base import get_data, make_layergroup, make_feature

import logging
log = logging.getLogger(__file__)


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


def create_coverages_dir(data_dir, aerials_dir):
    """
    does 2 things:
      1. create the data_dir/coverages folder
      2. create a soft link in data_dir/coverages to the geotiff 'aerials_dir' 
         (e.g., ln -s ~/aerials data_dir/coverages/aerials)
    """
    coverage_dir = os.path.join(data_dir, "coverages")
    aerials_link = os.path.join(coverage_dir, os.path.basename(aerials_dir))
    Path(coverage_dir).mkdir(exist_ok=True)
    Path(aerials_link).unlink(missing_ok=True)
    Path(aerials_link).symlink_to(Path(aerials_dir))


def generate_geoserver_aerial_config(data_dir="data_dir"):
    """
    defacto main statment to generate the config for aerials in the geoserver data_dir
    """
    def_params = {}
    def_params['dir'] = data_dir

    from ott.utils.parse.cmdline import osm_cmdline
    parser = osm_cmdline.geoserver_parser(def_params, "poetry run generate-geoserver-aerial-config", False)
    parser.add_argument(
        '--aerials_dir',
        '-aerials',
        '-ad',
        required=False,
        default=os.path.join(Path.home(), "aerials"),
        help="the directory where the geotiff aerials live"
    )
    args = parser.parse_args()

    #import pdb; pdb.set_trace()
    create_coverages_dir(args.data_dir, args.aerials_dir)

