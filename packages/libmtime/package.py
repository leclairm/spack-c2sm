class Libmtime(AutotoolsPackage):
    """Time management library. This project aims to provide time, calendar,
    and event handling for model applications."""

    homepage = 'https://code.mpimet.mpg.de/projects/mtime'
    git = 'git@gitlab.dkrz.de:icon-libraries/libmtime.git'

    version('1.0.8-p1', branch='1.0.8-patched')

    variant('openmp', default=False,
            description='Ensure compatibility with OpenMP applications')
    variant('examples', default=True, description='Build examples')

    depends_on('libcheck', type='test')

    def configure_args(self):
        config_args = self.enable_or_disable('examples')
        config_args += self.enable_or_disable('openmp')

        if self.run_tests:
            config_args.extend(
                ['--enable-check',
                 '--with-check-root=%s' % self.spec['libcheck'].prefix])
        else:
            config_args.append('--disable-check')

        return config_args
