from spack.util.environment import is_system_path


class Libcdi(AutotoolsPackage):
    """CDI is a C and Fortran Interface to access Climate and NWP model Data.
    Supported data formats are GRIB, netCDF, SERVICE, EXTRA and IEG."""

    homepage = 'https://code.mpimet.mpg.de/projects/cdi'
    git = 'https://gitlab.dkrz.de/mpim-sw/libcdi.git'

    version('1.8.x', branch='cdi-1.8.x')

    variant('shared', default=True, description='Enable shared libraries')
    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('grib2',
            default='eccodes',
            values=('eccodes', 'grib-api', 'none'),
            description='Specify GRIB2 backend')
    variant('external-grib1',
            default=False,
            description='Ignore the built-in support and use the external '
            'GRIB2 backend for GRIB1 files')
    variant('szip-grib1',
            default=False,
            description='Enable szip compression for GRIB1')
    variant('fortran', default=True, description='Enable Fortran interfaces')
    variant('threads',
            default=True,
            description='Compile and link for multithreading')

    depends_on('netcdf-c', when='+netcdf')
    # The library implicitly links to HDF5 when NetCDF support is enabled
    depends_on('hdf5', when='+netcdf')

    depends_on('grib-api', when='grib2=grib-api')
    depends_on('eccodes', when='grib2=eccodes')

    depends_on('szip', when='+szip-grib1')

    depends_on('uuid')

    conflicts('+szip-grib1',
              when='+external-grib1 grib2=none',
              msg='The configuration does not support GRIB1')

    conflicts('^ossp-uuid', msg='OSSP uuid is not currently supported')

    @property
    def libs(self):
        lib_names = []
        if 'fortran' in self.spec.last_query.extra_parameters:
            lib_names.append('libcdi_f2003')
        lib_names.append('libcdi')

        shared = '+shared' in self.spec
        libs = find_libraries(lib_names,
                              root=self.prefix,
                              shared=shared,
                              recursive=True)

        if libs:
            return libs

        msg = 'Unable to recursively locate {0} libraries in {1}'
        raise spack.error.NoLibrariesError(
            msg.format(self.spec.name, self.spec.prefix))

    def configure_args(self):
        config_args = [
            # Always build static libraries
            '--enable-static',
            # Use the service library
            '--enable-service',
            # Use the extra library
            '--enable-extra',
            # Use the ieg library
            '--enable-ieg',
            # Disable HIRLAM extensions
            '--disable-hirlam-extensions',
            # Disable MPI support
            '--disable-mpi',
            # Due to a bug in the configure script we have to avoid explicit
            # disabling of swig-based, ruby and python bindings with
            # '--disable-swig', '--disable-ruby', and '--disable-python'.
        ]

        config_args += self.enable_or_disable('shared')

        # Help Libtool to find the right UUID library
        libs = self.spec['uuid'].libs

        config_args += self.with_or_without('threads')

        if '+netcdf' in self.spec:
            config_args.append('--with-netcdf=' + self.spec['netcdf-c'].prefix)
            # Help Libtool to find the right HDF5 library
            libs += self.spec['hdf5'].libs
        else:
            config_args.append('--without-netcdf')

        if self.spec.variants['grib2'].value == 'eccodes':
            libs += self.spec['eccodes'].libs
            config_args.append('--with-grib_api')
        elif self.spec.variants['grib2'].value == 'grib-api':
            config_args.append('--with-grib_api=' +
                               self.spec['grib-api'].prefix)
        else:
            config_args.append('--without-grib_api')

        if '+external-grib1' in self.spec:
            config_args.append('--disable-cgribex')
        else:
            config_args.append('--enable-cgribex')

        if '+szip-grib1' in self.spec:
            config_args.append('--with-szlib=' + self.spec['szip'].prefix)
        else:
            config_args.append('--without-szlib')

        if '+fortran' in self.spec:
            config_args.extend(
                ['--enable-iso-c-interface', '--enable-cf-interface'])
        else:
            config_args.extend(
                ['--disable-iso-c-interface', '--disable-cf-interface'])

        # We do not use libs.search_flags because we need to filter the system
        # directories out.
        config_args.extend([
            'LDFLAGS={0}'.format(' '.join([
                '-L' + d for d in libs.directories if not is_system_path(d)
            ])), 'LIBS={0}'.format(libs.link_flags)
        ])

        return config_args
