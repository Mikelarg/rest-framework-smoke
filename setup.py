import os
import re
import subprocess
from pathlib import Path

from setuptools import setup  # type: ignore

with open('README.md') as f:
    long_description = f.read()

version_re = re.compile('^Version: (.+)$', re.M)
package_name = 'rest-framework-smoke'


def get_version():
    """
    Reads version from git status or PKG-INFO

    https://gist.github.com/pwithnall/7bc5f320b3bdf418265a
    """
    d: Path = Path(__file__).absolute().parent
    git_dir = d.joinpath('.git')
    if git_dir.is_dir():
        # Get the version using "git describe".
        cmd = 'git describe --tags --match [0-9]*'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate a
        # development revision after the release.
        with open(os.devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        if dirty != '':
            version += '.dev1'
    else:
        # Extract the version from the PKG-INFO file.
        try:
            with open('PKG-INFO') as v:
                version = version_re.search(v.read()).group(1)
        except FileNotFoundError:
            version = None

    return version


setup(
    name=package_name,
    version=get_version() or 'dev',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['rest_framework_smoke.tests'],
    url='https://github.com/just-work/rest-framework-smoke',
    license='MIT',
    author='Sergey Tikhonov',
    author_email='zimbler@gmail.com',
    description='Smoke tests for API built with Django Rest Framework',
    install_requires=[
        'Django',
        'djangorestframework',
        'jsonschema',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Testing',
    ]
)
