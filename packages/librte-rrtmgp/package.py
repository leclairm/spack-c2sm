class LibrteRrtmgp(AutotoolsPackage):
    """A set of codes for computing radiative fluxes in planetary
    atmospheres."""

    homepage = 'https://github.com/RobertPincus/rte-rrtmgp'
    git = 'https://github.com/RobertPincus/rte-rrtmgp.git'

    version('icon', branch='icon-integration')
    version('master', branch='autoconf')

    variant('openacc', default=False, description='Enable OpenACC kernels')

    depends_on('python', type='build')

    depends_on('netcdf-fortran', type='test')
    depends_on('python@3:', type='test')
    depends_on('py-netcdf4', type='test')
    depends_on('py-xarray@0.12.2:', type='test')
    depends_on('py-dask+array', type='test')

    @property
    def libs(self):
        return find_libraries(['librte', 'librrtmgp'],
                              root=self.prefix.lib,
                              shared=False)

    def configure_args(self):
        args = self.enable_or_disable('openacc')
        if self.run_tests:
            args.extend([
                '--enable-tests',
                '--with-netcdf-fortran=%s' % self.spec['netcdf-fortran'].prefix
            ])

        return args
