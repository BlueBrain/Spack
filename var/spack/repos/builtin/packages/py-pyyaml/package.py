# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyyaml(PythonPackage):
    """PyYAML is a YAML parser and emitter for Python."""
    homepage = "http://pyyaml.org/wiki/PyYAML"
    url      = "http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz"

    version('5.1.2', sha256='01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4')
    version('3.13', sha256='3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf')
    version('3.12', '4c129761b661d181ebf7ff4eb2d79950')
    version('3.11', 'f50e08ef0fe55178479d3a618efe21db')
