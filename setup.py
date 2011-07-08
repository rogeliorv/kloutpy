#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) - 2009 Juan B Cabral <jbc dot develop at gmail dot com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#==============================================================================
# DOCS
#==============================================================================

"""Setup for kloutpy"""

#==============================================================================
# IMPORTS
#==============================================================================

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
import kloutpy
import test



#==============================================================================
# SETUP
#==============================================================================

name = "kloutpy"

version = str(kloutpy.__version__)

download_url = "https://bitbucket.org/leliel12/kloutpy/get/%s.tar.gz#egg=%s-%s" % (version,
                                                                                   name,
                                                                                   version)

setup(name=name,
      version=version,
      description="Python Klout (http://klout.com/) api",
      author="JBC",
      author_email="jbc dot develop at gmail dot com",
      url="https://bitbucket.org/leliel12/kloutpy",
      download_url=download_url,
      license="LGPL3",
      keywords="klout",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Natural Language :: Spanish",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Topic :: Internet",
                   "Topic :: Internet :: WWW/HTTP", 
                   ],
      py_modules = ['kloutpy'],
)


#==============================================================================
# MAIN
#==============================================================================

if __name__ == '__main__':
    print(__doc__)
