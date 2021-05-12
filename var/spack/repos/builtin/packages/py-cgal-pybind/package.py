# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCgalPybind(PythonPackage):
    """Internal Python bindings for CGAL"""

    homepage = "https://bbpcode.epfl.ch/browse/code/common/cgal-pybind/tree/"

    version("develop", submodules=True)
    version(
        "0.1.0",
        tag="cgal_pybind-v0.1.0",
        submodules=True,
        git="git@bbpgitlab.epfl.ch:nse/cgal-pybind.git",  # migration to gitlab
    )
    version(
        "0.0.2",
        commit="7aa1382d1628ccd51f692750a2b145b1df0694d9",
        submodules=True,
        git="ssh://bbpcode.epfl.ch/common/cgal-pybind",
    )

    depends_on("py-setuptools", type="build")
    depends_on("boost@1.50:")
    depends_on("cmake", type="build")
    depends_on("cgal")
    depends_on("eigen")
    depends_on("py-pybind11")
    depends_on("py-numpy@1.12:", type=("build", "run"))
