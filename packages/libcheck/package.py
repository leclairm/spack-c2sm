class Libcheck(AutotoolsPackage):
    """A unit testing framework for C."""

    homepage = "https://libcheck.github.io/check/index.html"
    url = "https://github.com/libcheck/check/releases/download/0.12.0/check-0.12.0.tar.gz"

    depends_on('pkgconfig', type='build')

    version('0.12.0', '31b17c6075820a434119592941186f70')
