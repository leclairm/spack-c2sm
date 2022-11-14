class IconDev(BundlePackage):
    """ICON (Icosahedral Nonhydrostatic Weather and Climate Model) development
    environment."""

    homepage = "https://code.mpimet.mpg.de/projects/iconpublic"

    version('master')

    # Model features (only those that might trigger additional software
    # dependencies or constraints):
    variant('coupling', default=True, description='Enable the coupling')
    variant('ecrad',
            default=False,
            description='Enable usage of the ECMWF radiation scheme (ECRAD)')
    variant('rte-rrtmgp',
            default=False,
            description='enable usage of the RTE+RRTMGP toolbox for radiation '
            'calculations')
    variant(
        'rttov',
        default=False,
        description='Enable usage of the radiative transfer model for TOVS')
    variant('dace',
            default=False,
            description='Enable the DACE modules for data assimilation')
    variant('emvorado',
            default=False,
            description='Enable the radar forward operator EMVORADO')
    variant('art',
            default=False,
            description='Enable the aerosols and reactive trace component ART')

    # Infrastructural Features (only those that might trigger additional
    # software dependencies or contraints):
    variant('mpi',
            default=True,
            description='Enable MPI (parallelization) support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('gpu', default=False, description='Enable GPU support')
    variant('grib2',
            default='eccodes',
            values=('none', 'eccodes', 'grib-api'),
            description='Enable GRIB2 I/O using the specified backend')
    variant('parallel-netcdf',
            default=False,
            description='Enable usage of the parallel features of NetCDF')
    variant('cdi-pio',
            default=False,
            description='Enable usage of the parallel features of CDI')
    variant('sct', default=False, description='Enable the SCT timer')
    variant('yaxt', default=True, description='Enable the YAXT data exchange')
    variant('claw', default=False, description='Enable CLAW preprocessing')
    variant('serialization',
            default=False,
            description='Enable the Serialbox2 serialization')

    for bundled_lib in [
            'ecrad', 'rte-rrtmgp', 'sct', 'yaxt', 'cdi', 'mtime', 'yac',
            'tixi', 'self', 'cub'
    ]:
        variant('external-{0}'.format(bundled_lib),
                default=False,
                description='use external {0} library '.format(
                    bundled_lib.upper()))

    conflicts('+external-tixi',
              when='~art',
              msg='external TIXI is not required when ART is disabled')
    conflicts('+externals-yac',
              when='~coupling',
              msg='external YAC is not required when the coupling is disabled')
    conflicts('+external-yac',
              when='~external-mtime',
              msg='building with external YAC requires '
              'building with external MTIME')
    conflicts('+coupling',
              when='~mpi',
              msg='building with the coupling requires '
              'building with MPI support')
    conflicts('+cdi-pio',
              when='~external-cdi',
              msg='building with the parallel features of CDI requires '
              'building with external CDI')
    conflicts('+cdi-pio',
              when='~mpi',
              msg='building with the parallel features of CDI requires '
              'building with MPI support')
    conflicts('+yaxt',
              when='~mpi',
              msg='building with the YAXT data exchange requires '
              'building with MPI support')
    conflicts('+parallel-netcdf',
              when='~mpi',
              msg='building with the parallel features of NetCDF requires '
              'building with MPI support')
    conflicts('+external-yaxt',
              when='~cdi-pio~yaxt',
              msg='external YAXT is not required when both the parallel '
              'features of CDI and the YAXT data exchange are disabled')
    conflicts(
        '+external-sct',
        when='~sct',
        msg='external SCT is not required when the SCT timer is disabled')
    conflicts('+external-ecrad',
              when='~ecrad',
              msg='external ECRAD is not required when the ECMWF radiation '
              'scheme (ECRAD) is disabled')
    conflicts('+external-rte-rrtmgp',
              when='~rte-rrtmgp',
              msg='external RTE-RRTMGP is not required when the RTE+RRTMGP '
              'toolbox for radiation calculations is disabled')
    conflicts('+external-cub',
              when='~gpu',
              msg='external CUB is not required when GPU support is disabled')
    conflicts('+gpu',
              when='~claw',
              msg='building with GPU support requires '
              'building with CLAW preprocessing')

    depends_on('libself', when='+external-self')
    depends_on('libicon-tixi', when='+external-tixi')
    depends_on('yac+xml+netcdf+external-mtime+mpi lapack=fortran',
               when='+external-yac')
    depends_on('libmtime', when='+external-mtime')
    depends_on('libmtime+openmp', when='+external-mtime+openmp')
    depends_on('serialbox', when='+serialization')

    for grib2_backend in ['none', 'eccodes', 'grib-api']:
        depends_on(
            'libcdi+fortran+netcdf grib2={0}'.format(grib2_backend),
            when='+external-cdi~cdi-pio grib2={0}'.format(grib2_backend))
        depends_on('libcdi-pio+fortran+netcdf grib2={0}'.format(grib2_backend),
                   when='+cdi-pio grib2={0}'.format(grib2_backend))

    depends_on('eccodes+fortran', when='+emvorado grib2=eccodes')
    depends_on('grib-api+fortran', when='+emvorado grib2=grib-api')
    depends_on('eccodes', when='~external-cdi grib2=eccodes')
    depends_on('grib-api', when='~external-cdi grib2=grib-api')

    depends_on('yaxt', when='+external-yaxt')

    depends_on('libsct+hdf5', when='+external-sct')
    depends_on('libsct+openmp', when='+external-sct+openmp')
    depends_on('libsct+mpi', when='+external-sct+mpi')

    # Not available yet
    # depends_on('librttov', when='+rttov')

    depends_on('lapack')
    depends_on('blas')

    depends_on('libecrad', when='+external-ecrad')

    depends_on('librte-rrtmgp+openacc', when='+external-rte-rrtmgp+gpu')
    depends_on('librte-rrtmgp~openacc', when='+external-rte-rrtmgp~gpu')

    depends_on('netcdf-fortran')

    depends_on('netcdf-c', when='~external-cdi')
    depends_on('netcdf-c+mpi', when='+parallel-netcdf')

    depends_on('hdf5+hl+fortran', when='+emvorado')
    depends_on('hdf5+hl+fortran', when='+rttov')
    depends_on('hdf5', when='+sct~external-sct')

    depends_on('zlib', when='+emvorado')

    depends_on('mpi', when='+mpi')

    depends_on('cub', when='+external-cub')

    depends_on('cuda', when='+gpu')

    depends_on('claw', when='+claw')

    depends_on('python')
    depends_on('perl')
