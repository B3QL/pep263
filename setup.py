"""Package configuration."""
import os
import re

from setuptools import find_packages, setup


def find_version(*file_paths):
    """Find version information in file."""
    path = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(path).read()
    version_pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(version_pattern, version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


tests_requirements = [
    'pytest==3.6.0',
    'pylama==7.4.3',
    'pylint==1.9.1',
    'pylama-pylint==3.0.1',
]

setup(
    name='pep263',
    version=find_version('pep263', '__init__.py'),
    author='Bartłomiej Kurzeja',
    url='https://github.com/B3QL/pep263',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'click==6.7',
        'colorama==0.3.9',
    ],
    tests_require=tests_requirements,
    extras_require={
        ':python_version<"3.5"': ["scandir==1.7"],
        'test': tests_requirements,
    },
    entry_points={
        'console_scripts': [
            'pep263=pep263.cli:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
