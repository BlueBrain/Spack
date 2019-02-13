# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Basalt(PythonPackage):
    """C++11 Graph Storage library with Python interface"""

    homepage = "https://github.com/tristan0x/basalt"
    url      = "git@github.com:tristan0x/basalt.git"
    
    version('develop', git=url, branch='master', submodules=True)
    version('0.1.1', git=url, tag='v0.1.1', submodules=True, preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('rocksdb~static')
    depends_on('python@3:')
    depends_on('cmake@3.5:')
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-humanize', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('benchmark')
