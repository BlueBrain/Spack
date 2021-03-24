# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git      = "https://github.com/BlueBrain/morph-tool.git"
    url      = "https://pypi.io/packages/source/m/morph-tool/morph-tool-0.2.5.tar.gz"

    version('develop', branch='master')
    version('2.4.0', sha256='268915ad48f2a2475bbc4685bd1a3610f22978fee1cb4d376d87f45ae4a028e1')
    version('2.2.21', sha256='37d932b8b9561d9b5b4d0d3cdb1b146e9d4e3443526b8ef6e88aeeac36528c7e')
    version('0.2.10', sha256='e46835b9c25532cbee070141ad9f7d3d47109d5473074b47aad08f51bdc40157')
    version('0.2.5', sha256='7157039a7a421cfbdb75fd305975a6e6ce7667177dc68bd299645b62389622be')
    version('0.2.3', sha256='767effaa4d2e8c7dfee878c6d48c6647f29b19fee6f790213783c04d8951fee3')
    version('0.2.1', tag='morph-tool-v0.2.1', git='ssh://bbpcode.epfl.ch/nse/morph-tool')
    version('0.1.14', tag='morph-tool-v0.1.14', git='ssh://bbpcode.epfl.ch/nse/morph-tool')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('neuron+python', when='@0.2.1:', type='run')
    depends_on('py-bluepyopt@1.9.37:', type='run', when='@0.2.1:')
    depends_on('py-click@7.0:', type='run')
    depends_on('py-functools32', when='@:0.2.3^python@:2.99', type='run')
    depends_on('py-morphio@2.7.0:', type='run')
    depends_on('py-neurom@1.8.0:', type='run', when='@0.1.14:')
    depends_on('py-pathlib2@2.3.5:', when='@:0.2.3^python@:2.99', type='run')
    depends_on('py-pyyaml', when='@:0.1.14', type='run')
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@1.0.3:', when='@0.2.5:', type='run')
    depends_on('py-dask@2.19:', when='@0.2.10:', type='run')
    depends_on('py-plotly@4.1:', when='@0.2.10:', type='run')
    depends_on('py-xmltodict@0.12:', when='@0.2.10:', type='run')

    depends_on('py-deprecation@2.1.0:', when='@2.4.0:', type='run')
    depends_on('py-more-itertools@8.6.0:', when='@2.4.0:', type='run')
