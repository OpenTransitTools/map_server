import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'pystache',

    'MapProxy',

    # added Nov 2019 ... 'venusian==3.0.0' is python 3.x, so won't work with Py 2.7
    'pillow<7.0.0',
    'pyproj<2.2.5',
    'venusian==1.2.0',

    'pyramid',
    'pyramid_tm',
    'pyramid_exclog',
    'waitress',
]

extras_require = dict(
    dev=[],
)

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])

setup(
    name='ott.map_server',
    version='0.1.0',
    description='Open Transit Tools - OTT Map Server',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=[
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
    ],
    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, gtfs, gtfsdb, data, database, services, transit, geo, geoserver',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.map_server.tests",
    # find ott | grep py$ | xargs grep "def.main"
    entry_points="""
        [paste.app_factory]
        main = ott.map_server.pyramid.app:main
        [console_scripts]
        generate_geoserver_config = ott.map_server.geoserver_config.base:generate_geoserver_config
        run_jetty_config = ott.map_server.geoserver_config.jetty_config:run_jetty_config
        mapproxy = mapproxy.script.util:main
    """,
    #   bin/mapproxy serve-develop mapproxy/mapproxy.yaml  --address 127.0.0.1:2112 # default port is 8080
)
