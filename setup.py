"""Package configuration."""
import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def find_version(*file_paths):
    """Find version information in file."""
    path = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(path).read()
    version_pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(version_pattern, version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class PyTest(TestCommand):
    """Pytest tests runner."""

    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def __init__(self, *args, **kwargs):
        """Initalize."""
        super(PyTest, self).__init__(*args, **kwargs)
        self.pytest_args = ''

    def run_tests(self):
        """Run tests."""
        import shlex
        import pytest  # import here, cause outside the eggs aren't loaded
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


test_requirements = [
    'pytest==3.6.0',
    'pylama==7.4.3',
    'pylint==1.9.1',
    'pylama-pylint==3.0.1',
]

setup(
    name='pep263',
    version=find_version('pep263', '__init__.py'),
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
