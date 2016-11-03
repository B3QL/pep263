import os
import re
from setuptools import setup, find_packages


def find_version(*file_paths):
    path = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(path).read()
    version_pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(version_pattern, version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='pep263',
    version=find_version('pep263', '__init__.py'),
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests*']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
