#!/usr/bin/python3

# Tests that ICON can be installed.

import subprocess
import unittest


class IconTest(unittest.TestCase):

    def test_nwp(self):
        subprocess.run('spack install icon @nwp', check=True, shell=True)


if __name__ == '__main__':
    unittest.main()
