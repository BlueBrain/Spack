# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Spack Project Developers. See the top-level COPYRIGHT file for details.
import os
import shutil
import llnl.util.tty as tty
from spack import *
from spack.pkg.builtin.sim_model import SimModel

# Definitions
_CORENRN_MODLIST_FNAME = "coreneuron_modlist.txt"


class NeurodamusCore(SimModel):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"

    version('optional_mpi', branch='sandbox/leite/optional_mpi', clean=False)
    version('2.8.0', tag='2.8.0', clean=False)
    version('2.7.3', tag='2.7.3', clean=False)
    version('2.7.2', tag='2.7.2', clean=False)
    version('2.7.0', tag='2.7.0', clean=False)
    version('2.6.0', tag='2.6.0', clean=False)
    version('2.5.0', tag='2.5.0', clean=False)
    version('2.4.3', tag='2.4.3', clean=False)
    version('2.4.1', tag='2.4.1', clean=False)
    version('2.3.4', tag='2.3.4', clean=False)
    version('2.3.3', tag='2.3.3', clean=False)
    version('2.2.1', tag='2.2.1', clean=False)

    variant('mpi',    default=True, description="Enable MPI support")
    variant('common', default=False, description="Bring in common synapse mechanisms")
    variant('hdf5',   default=True, description="Enable old Hdf5 reader")
    variant('reportinglib', default=True, description="Enable ReportingLib")
    variant('synapsetool',  default=True, description="Enable SynapseTool reader (for edges)")
    variant('mvdtool',      default=False, description="Enable MVDTool reader (for nodes)")

    # NOTE: Several variants / dependencies come from SimModel
    depends_on("mpi", when='+mpi', type=('build', 'run'))  # dont link
    depends_on("hdf5", when='+hdf5')
    depends_on('reportinglib',         when='+reportinglib')
    depends_on('reportinglib+profile', when='+reportinglib+profile')
    depends_on('synapsetool',          when='+synapsetool')
    depends_on('py-mvdtool',           when='+mvdtool', type='run')
    # If external & static, we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    resource(name='common',
             git='ssh://bbpcode.epfl.ch/sim/models/common',
             when='+common',
             destination='resources')

    depends_on('python@2.7:', type=('build', 'run'))

    mech_name = "neurodamus"

    @run_before('build')
    def prepare(self):
        filter_file(r'UNKNOWN_CORE_VERSION', r'%s' % self.spec.version,
                    join_path('hoc', 'defvar.hoc'))
        try:
            commit_hash = self.fetcher[0].get_commit()
        except Exception as e:
            tty.warn("Error extracting commit hash: " + str(e))
        else:
            filter_file(r'UNKNOWN_CORE_HASH', r"'%s'" % commit_hash[:8],
                        join_path('hoc', 'defvar.hoc'))

        # '+common' will bring common mods.
        # Otherwise build purely neurodamus helper mechs
        if self.spec.satisfies('+common'):
            copy_all('resources/common/hoc', "hoc")
            copy_all('resources/common/mod', "mod")
        else:
            # These two mods are also part of common
            os.remove("mod/VecStim.mod")
            os.remove("mod/netstim_inhpoisson.mod")

        # If we shall build mods for coreneuron, only bring from core those specified
        if self.spec.satisfies("+coreneuron"):
            mkdirp("mod_core")
            with open(join_path("mod", _CORENRN_MODLIST_FNAME)) as core_mods:
                for aux_mod in core_mods:
                    modpath = join_path("mod", aux_mod.strip())
                    if os.path.isfile(modpath):
                        shutil.copy(modpath, 'mod_core')

    def build(self, spec, prefix):
        """ Build mod files from with nrnivmodl / nrnivmodl-core.
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        variant_to_compile_flag = {
            "~mpi": "-DDISABLE_MPI",
            "~hdf5": "-DDISABLE_HDF5",
            "~reportinglib": "-DDISABLE_REPORTINGLIB",
            "~synapsetool": "-DDISABLE_SYNTOOL"
        }

        compile_flags = " ".join(flag for variant, flag in variant_to_compile_flag.items()
                                 if spec.satisfies(variant))
        self._build_mods('mod', '', compile_flags, 'mod_core')

    # NOTE: install() is inherited

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        run_env.prepend_path('MOD_LIBRARY_PATH', self.prefix.share.mod)
        run_env.prepend_path("PYTHONPATH", self.prefix.lib.python)
        for lib in find(self.prefix.lib, 'libnrndamus*'):
            run_env.set('BGLIBPY_MOD_LIBRARY_PATH', lib)
