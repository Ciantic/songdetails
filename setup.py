#!/usr/bin/env python

import sys
assert sys.version >= '2.5', "Requires Python v2.5 or above"
from distutils.core import setup, Extension

setup(
    name="songdetails",
    version="0.1",
    author="Jari Pennanen",
    author_email="jari.pennanen@gmail.com",
    url="http://github.com/Ciantic/songdetails/",
    description="Song details retrieval package.",
    long_description="Retrieves Song detail information such as artist, title, album duration, etc.",
    license="FreeBSD",
    packages=['songdetails', 'songdetails.mp3details'],
    package_dir={'songdetails': 'src/songdetails'}
)
