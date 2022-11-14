from spack.util.environment import is_system_path


class LibiconTixi(AutotoolsPackage):
    """A limited version of the tixi library for ICON."""

    homepage = 'https://gitlab.dkrz.de/icon-libraries/libtixi'
    git = 'git@gitlab.dkrz.de:icon-libraries/libtixi.git'

    version('develop', branch='icon-new-config')

    depends_on('libxml2')

    def flag_handler(self, name, flags):
        if name == 'cppflags':
            # Account for the case when libxml2 is an external package installed
            # to a system directory, which means that Spack will not inject the
            # required -I flag with the compiler wrapper:
            xml2_spec = self.spec['libxml2']
            if is_system_path(xml2_spec.prefix):
                xml2_headers = xml2_spec.headers
                # We, however, should filter the pure system directories out:
                xml2_headers.directories = [d for d in xml2_headers.directories
                                            if not is_system_path(d)]
                flags.append(xml2_headers.cpp_flags)

        return flags, None, None
