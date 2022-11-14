from collections import defaultdict

from spack.util.environment import is_system_path


class Extpar(AutotoolsPackage):
    """EXTPAR (External Parameters for Numerical Weather Prediction and Climate
    Application) is an official software of the COSMO Consortium. It is used to
    prepare the external parameter data files that are used as input for the
    COSMO model, and additionally now the ICON model."""

    homepage = 'http://www.cosmo-model.org/content/support/software/default.htm#extpar'
    git = 'git@github.com:C2SM-RCM/extpar.git'

    version('master', branch='master', submodules=True)
    version('5.8.0', tag='v.5.8', submodules=True)
    version('5.4.0', tag='v5.4', submodules=True)

    variant('openmp', default=True, description='enable OpenMP support')

    depends_on('python', type='build')

    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('hdf5')

    patch('gen_info/5.4.0.patch', when='@:5.4')
    patch('gen_info/5.5.0.patch', when='@5.5:')
    patch('cdi_linker_flags.patch', when='@:5.4.1')

    def configure_args(self):

        def yes_or_prefix(spec_name):
            prefix = self.spec[spec_name].prefix
            return 'yes' if is_system_path(prefix) else prefix

        args = [
            '--with-netcdf-fortran=%s' % yes_or_prefix('netcdf-fortran'),
            '--with-cdi=bundled',
            # Tune CDI:
            '--enable-cgribex',  # required by test_resource_copy_run
            '--disable-extra',
            '--enable-grib',  # required by test_resource_copy_run
            '--disable-ieg',
            '--disable-service',
            '--disable-util-linux-uuid',
            '--disable-ossp-uuid',
            '--disable-dce-uuid',
            '--without-eccodes',
            '--without-grib_api',
            '--without-szlib',
            # Version of CDI that is currently in use depends on pthread
            # library even when thread support is disabled. Therefore, we have
            # to enable threads explicitly, so that the configure script of
            # extpar could get the required linker flags:
            '--with-threads',
            '--with-netcdf=%s' % yes_or_prefix('netcdf-c')]

        flags = defaultdict(list)

        # Help the libtool script of CDI to find the right HDF5 library:
        hdf5_spec = self.spec['hdf5']
        hdf5_libs = hdf5_spec.libs
        # The libtool script of CDI might trigger implicit linking to -lhdf5
        # (normally happens when netcdf.la is present). Make the linking
        # explicit:
        flags['LIBS'].append(hdf5_libs.link_flags)
        # Also help the libtool script of CDI to find the right library:
        if not is_system_path(hdf5_spec.prefix):
            flags['LDFLAGS'].append(hdf5_libs.search_flags)

        args += self.enable_or_disable('openmp')

        args.extend(['{0}={1}'.format(var, ' '.join(val))
                     for var, val in flags.items()])

        return args
