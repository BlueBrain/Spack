# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyToolz(PythonPackage):
    """A set of utility functions for iterators, functions, and dictionaries"""

    homepage = "http://github.com/pytoolz/toolz/"
    url      = "https://pypi.io/packages/source/t/toolz/toolz-0.9.0.tar.gz"

    import_modules = ['toolz', 'tlz', 'toolz.curried', 'toolz.sandbox']

    version('0.11.1', sha256='c7a47921f07822fe534fb1c01c9931ab335a4390c782bd28c6bcc7c2f71f3fbf')
    version('0.9.0', sha256='929f0a7ea7f61c178bd951bdae93920515d3fbdbafc8e6caf82d752b9b3b31c9')

    depends_on('py-setuptools', type='build')
