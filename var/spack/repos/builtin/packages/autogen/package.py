# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Autogen(AutotoolsPackage):
    """AutoGen is a tool designed to simplify the creation and maintenance of
    programs that contain large amounts of repetitious text. It is especially
    valuable in programs that have several blocks of text that must be kept
    synchronized."""

    homepage = "https://www.gnu.org/software/autogen/index.html"
    url      = "ftp://ftp.gnu.org/gnu/autogen/rel5.18.12/autogen-5.18.12.tar.gz"
    list_url = "https://ftp.gnu.org/gnu/autogen"
    list_depth = 1

    version('5.18.12', '551d15ccbf5b5fc5658da375d5003389')

    variant('xml', default=True, description='Enable XML support')

    depends_on('pkgconfig', type='build')

    depends_on('guile@1.8:2.0')
    depends_on('libxml2', when='+xml')

    def configure_args(self):
        spec = self.spec

        args = [
            # `make check` fails without this
            # Adding a gettext dependency does not help
            '--disable-nls',
        ]

        if '+xml' in spec:
            args.append('--with-libxml2={0}'.format(spec['libxml2'].prefix))
        else:
            args.append('--without-libxml2')

        return args
