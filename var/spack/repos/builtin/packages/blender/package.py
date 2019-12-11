# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.

from spack import *

import os
import shutil

class Blender(Package):
    """Blender is the free and open source 3D creation suite."""

    homepage = "https://www.blender.org"

    version('2.81a-217', sha256='bb6e03ef79d2d7273336f8cfcd5a3b3f')

    conflicts("python")

    def install(self, spec, prefix):
	for file in os.listdir(self.stage.source_path):
            src = os.path.join(self.stage.source_path, file)
            dst = os.path.join(prefix, file)
            if os.path.isdir(src):
                shutil.copytree(src, dst, False)
            else:
                shutil.copy2(src, dst)

    def setup_environment(self, spack_env, run_env):
        blender_python_path = os.path.join(prefix, self.version.string[:4], 'python/lib/python3.7')
        run_env.set('PYTHONPATH', blender_python_path)

    def url_for_version(self, version):
	(blender_version_full, glibc_version) = version.string.split('-')
	blender_version_minor = version.up_to(2)
	base_url = "https://ftp.nluug.nl/pub/graphics/blender/release/"
	return "{}Blender{}/blender-{}-linux-glibc{}-x86_64.tar.bz2".format(base_url,blender_version_minor,blender_version_full,glibc_version) 
