# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBglibpy(spack.PythonPackage):
    """Pythonic Blue Brain simulator access"""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/sim/BGLibPy"
    git = "ssh://bbpcode.epfl.ch/sim/BGLibPy"

    version('develop', branch='master')
    version(
        '4.0.27',
        commit='42d9c1f891ef1ec9af6d72c49ff3b7726a009951')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('neuron+python~mpi', type='run')
    depends_on('py-h5py~mpi@2.3:', type='run')

    depends_on('py-bluepy@0.13.2:', type='run')
