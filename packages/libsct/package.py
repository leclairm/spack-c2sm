import glob


class Libsct(AutotoolsPackage):
    """The SCT library was invented with the aim of having an easy to use timer
    with as little overhead as possible."""

    homepage = 'https://code.mpimet.mpg.de/projects/performance-monitoring/wiki/Access_of_stored_performance_data'
    git = 'https://gitlab.dkrz.de/dkrz-sw/sct.git'

    version('master', branch='master')

    variant('mpi', default=True, description='Enable MPI support')
    variant('openmp', default=True, description='Enable OpenMP parallel timer')
    variant('hdf5', default=True, description='Enable HDF5 output')
    variant('papi', default=False, description='Enable PAPI')
    variant('debug', default=False, description='Enable debug bode')
    variant('check-timer',
            default=False,
            description='Allow to check usage of sct (reduces the accuracy '
            'of the performance measurements)')
    variant('nested-timer',
            default=True,
            description='Enable timer nesting in reports (nested timer cannot '
            'be stopped while superordinate timer is still active)')
    variant('timestamp-counter',
            default=False,
            description='Enable timer based on the processor'
            's time-stamp '
            'counter (a 64-bit MSR) if accessible')
    variant('fakelib',
            default=False,
            description='Build additional fake libsct with same Fortran '
            'interface but without backend')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    depends_on('perl', type='test')

    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('papi', when='+papi')

    conflicts('+openmp',
              when='%clang platform=darwin',
              msg='OpenMP is not supported by Apple\'s clang.')

    # We need a solution for the problem reported in
    # https://gitlab.dkrz.de/dkrz-sw/sct/-/merge_requests/7
    # The developers declined the merge request and suggested using pgcc18.
    # However, the solution does not work but leads to other errors:
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 799)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 799)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 819)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 819)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 820)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 820)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 822)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 822)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 823)
    # PGCC-S-0061-Sizeof dimensionless array  required (sct_reporter.c: 823)
    # Therefore, we simply apply the changes from the merge request here:
    patch('pgi.patch', when='%pgi@:19')

    # Skip parallel tests if a working MPI_LAUNCH command not found and run all
    # of them with MPI_LAUNCH otherwise:
    patch('mpirun.patch', when='+mpi')

    def patch(self):
        # Patch long shebangs
        files = glob.glob('tests/test_*_run.in')
        filter_file(r'^#!\s*@PERL@\s*$', '#!/usr/bin/env perl', *files)

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    def configure_args(self):
        args = self.enable_or_disable('openmp')
        args += self.enable_or_disable('debug')
        args += self.enable_or_disable('check-timer')
        args += self.enable_or_disable('nested-timer')
        args += self.enable_or_disable('timestamp-counter')
        args += self.enable_or_disable('fakelib')

        if '+mpi' in self.spec:
            # MPICC, CC and FC are set by Spack
            args += ['--enable-mpi', 'MPIFC=' + self.spec['mpi'].mpifc]
        else:
            args.append('--disable-mpi')

        if '+hdf5' in self.spec:
            args += [
                '--enable-hdf5',
                '--with-libhdf5-prefix=' + self.spec['hdf5'].prefix
            ]
        else:
            args.append('--disable-hdf5')

        if '+papi' in self.spec:
            args += [
                '--enable-papi',
                '--with-libpapi-prefix=' + self.spec['papi'].prefix
            ]
        else:
            args.append('--disable-papi')

        return args
