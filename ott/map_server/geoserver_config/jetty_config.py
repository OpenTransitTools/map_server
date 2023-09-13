import os
from ott.utils import file_utils
from ott.utils.parse.cmdline import osm_cmdline


def run_jetty_config():
    args = osm_cmdline.geoserver_parser("bin/run_jetty_config", def_dir="geoserver/webapps/geoserver/WEB-INF")

    # step 1: enable CORS in web.xml (note there are 2 places to uncomment CORS in web.xml)xx
    web_xml = os.path.join(args.data_dir, "web.xml")
    cmt = "Uncomment following filter to enable CORS"
    file_utils.uncomment_block_xml(web_xml, comment_regex=cmt)
    file_utils.uncomment_block_xml(web_xml, comment_regex=cmt)
