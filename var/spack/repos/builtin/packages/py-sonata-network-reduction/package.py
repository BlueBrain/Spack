# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySonataNetworkReduction(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/sonata-network-reduction"
    git      = "ssh://bbpcode.epfl.ch/nse/sonata-network-reduction"

    version('develop', branch='master')
    version('0.0.5', tag='sonata-network-reduction-v0.0.5')
    version('0.0.4', tag='sonata-network-reduction-v0.0.4')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-h5py@2.8:', type='run')
    depends_on('py-pandas@0.23:0.30', type='run')
    depends_on('py-lxml@4.3.4:', type='run')
    depends_on('py-tqdm@4.34:', type='run')
    depends_on('py-click@6.7:', type='run')
    depends_on('py-joblib@0.14:', type='run')
    depends_on('py-bluepyopt@1.8.68:', type='run')
    depends_on('py-bglibpy@4.2:', type='run')
    depends_on('py-morphio@2.3.4:', type='run')
    depends_on('neuron+python', type='run')
    depends_on('py-aibs-circuit-converter@0.0.1', type='run')
    depends_on('py-bluepysnap@0.1.2:', type='run')
    depends_on('py-neuron-reduce@0.0.7:', type='run')

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
