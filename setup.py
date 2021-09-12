#!/usr/bin/env python3

import sys, os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if not sys.version_info[0] == 3:
    sys.exit("Python 2.x is not supported; Python 3.x is required.")

########################################

setup(
    name="transmission-dump",
    version="0.1",
    description="Dump the contents of state files used by the Transmission BitTorrent client (dht.dat and *.resume)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Lenski",
    author_email="dlenski@gmail.com",
    license='GPL v3 or later',
    install_requires=open("requirements.txt").read().splitlines(),
    url="https://github.com/dlenski/transmission-dump",
    packages=['transmission_dump'],
    entry_points={ 'console_scripts': [
        'transmission-dump-dht=transmission_dump.dht:main',
        'transmission-dump-resume=transmission_dump.resume:main',
    ] },
)
