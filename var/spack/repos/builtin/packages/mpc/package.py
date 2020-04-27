# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import string

class Mpc(AutotoolsPackage):
    """Gnu Mpc is a C library for the arithmetic of complex numbers
       with arbitrarily high precision and correct rounding of the
       result."""

    homepage = "http://www.multiprecision.org"
    url      = "https://ftpmirror.gnu.org/mpc/mpc-1.1.0.tar.gz"
    list_url = "http://www.multiprecision.org/mpc/download.html"

    version('1.1.0a', sha256='6985c538143c1208dcb1ac42cedad6ff52e267b47e5f970183a3e75125b43c2e')
    version('1.0.3', sha256='617decc6ea09889fb08ede330917a00b16809b8db88c29c31bfbb49cbf88ecc3')
    version('1.0.2', sha256='b561f54d8a479cee3bc891ee52735f18ff86712ba30f036f8b8537bae380c488')

    # Could also be built against mpir instead
    depends_on('gmp@4.3.2:')
    depends_on('gmp@5.0.0:', when='@1.1.0:')
    depends_on('mpfr@2.4.2:')
    depends_on('mpfr@3.0.0:', when='@1.1.0:')

    def url_for_version(self, version):
        if version[-1] in string.ascii_letters:
            version = version[0:-1].strip()

        if version < Version("1.0.1"):
            url = "http://www.multiprecision.org/mpc/download/mpc-{0}.tar.gz"
        else:
            url = "https://ftpmirror.gnu.org/mpc/mpc-{0}.tar.gz"

        return url.format(version)

    def configure_args(self):
        spec = self.spec
        return [
            '--with-mpfr={0}'.format(spec['mpfr'].prefix),
            '--with-gmp={0}'.format(spec['gmp'].prefix)
        ]
