# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonKeycloak(PythonPackage):
    """Python package providing access to the Keycloak API."""

    homepage = "https://python-keycloak.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-keycloak/python-keycloak-0.17.2.tar.gz"

    version('0.17.2', sha256='56300a3ede3732b8a8f5a9936e6d1ddac5e704bd64af876c99eb34bb8c50eebc')

    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type='run')
    depends_on('py-python-jose', type='run')
