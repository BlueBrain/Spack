# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAibsCircuitConverter(PythonPackage):
    """Pythonic API for conversion between Allen Institute and BBP"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/aibs-circuit-converter"
    git      = "ssh://bbpcode.epfl.ch/nse/aibs-circuit-converter"

    version('develop', branch='master')
    version('0.0.1', sha256='f5dbf27d3c9752e5e593fff88a15acaebba159db')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.17:', type='run')
    depends_on('py-h5py@2.9:', type='run')
    depends_on('py-pandas@0.25:0.30', type='run')
    depends_on('py-lxml@4.3.4:', type='run')
    depends_on('py-tqdm@4.34:', type='run')
    depends_on('py-transforms3d@0.3.1:', type='run')
    depends_on('py-six@1.0:', type='run')
    depends_on('py-bluepyopt@1.8.68:', type='run')
