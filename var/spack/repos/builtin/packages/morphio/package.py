# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Morphio(CMakePackage):
    """Library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO"
    git      = "https://github.com/BlueBrain/MorphIO.git"
    url      = "https://pypi.io/packages/source/m/morphio/MorphIO-3.1.1.tar.gz"

    version('develop', submodules=True)

    version('3.1.1', sha256="ad9f0e363f09f03c6eda54f5f3b006d204236677d2f2c9675421e0441033a503")
    version('2.7.1', sha256="3f3e2229da85e874527775fce080f712b6dc287edc44b90b6de35d17b34badff")

    variant('mpi', default=True, description="Build with MPI support")

    depends_on('cmake@3.2:', type='build')
    depends_on('hdf5')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = ['-DBUILD_BINDINGS:BOOL=OFF']
        if self.spec.satisfies("+mpi"):
            args += [
                '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx)
            ]
        return args
