class Libecrad(AutotoolsPackage):
    """ECMWF radiation scheme."""

    homepage = 'https://gitlab.dkrz.de/dwd-sw/libecrad'
    git = 'git@gitlab.dkrz.de:dwd-sw/libecrad.git'

    version('master', branch='master')
    version('1.4.1', tag='ecrad-1.4.1')
    version('1.3.0', tag='ecrad-1.3.0')

    variant('single-precision', default=False,
            description='switch to single precision')

    depends_on('netcdf-fortran')
    depends_on('python', type='build')

    patch('nag.patch', when='@1.3.0%nag')

    # https://gitlab.dkrz.de/dwd-sw/libecrad/-/merge_requests/44
    patch('endianness.patch', when='@1.4.1:')

    # https://gitlab.dkrz.de/dwd-sw/libecrad/-/merge_requests/43
    patch('print_matrix.patch', when='@master%nag')

    @property
    def libs(self):
        return find_libraries(
            ['libradiation', 'libifsrrtm', 'libutilities', 'libifsaux'],
            root=self.prefix.lib, shared=False)

    def configure_args(self):
        args = self.enable_or_disable('single-precision')
        args.append('--with-netcdf-root=%s' %
                    self.spec['netcdf-fortran'].prefix)
        return args
