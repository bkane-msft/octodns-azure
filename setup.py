from os import environ
from subprocess import CalledProcessError, check_output

from setuptools import find_packages, setup


def descriptions():
    with open('README.md') as fh:
        ret = fh.read()
        first = ret.split('\n', 1)[0].replace('#', '')
        return first, ret


def version():
    version = 'unknown'
    with open('octodns_azure/__init__.py') as fh:
        for line in fh:
            if line.startswith('__VERSION__'):
                version = line.split("'")[1]
                break

    # pep440 style public & local version numbers
    if environ.get('OCTODNS_RELEASE', False):
        # public
        return version
    try:
        sha = check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')[:8]
    except (CalledProcessError, FileNotFoundError):
        sha = 'unknown'
    # local
    return f'{version}+{sha}'


description, long_description = descriptions()

tests_require = ('pytest>=6.2.5', 'pytest-cov>=3.0.0', 'pytest-network>=0.0.1')

setup(
    author='Ross McFarland',
    author_email='rwmcfa1@gmail.com',
    description=description,
    extras_require={
        'dev': tests_require
        + (
            'black>=22.3.0',
            'build>=0.7.0',
            # >=5.12.0 does not support python 3.7, we still do
            'isort==5.11.5',
            # >=3.0.0 does not support python 3.7, we still do
            'markdown-it-py<3.0.0',
            'pyflakes>=2.2.0',
            'readme_renderer[md]>=26.0',
            'twine>=3.4.2',
        ),
        'test': tests_require,
    },
    install_requires=(
        'azure-identity>=1.7.1,<1.8.0',
        'azure-mgmt-dns>=8.1.0b1,<8.2.0',
        'azure-mgmt-privatedns>=1.0.0,<1.1.0',
        'azure-mgmt-trafficmanager>=1.1.0b1,<1.2.0',
        'msrestazure>=0.6.4,<0.7.0',
        'octodns>=0.9.16',
    ),
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='octodns-azure',
    packages=find_packages(),
    python_requires='>=3.6',
    tests_require=tests_require,
    url='https://github.com/octodns/octodns-azure',
    version=version(),
)
