# This is purely the result of trial and error.

import codecs
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import dateno


class PyTest(TestCommand):
    # `$ python setup.py test' simply installs minimal requirements
    # and runs the tests with no fancy stuff like parallel execution.
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './classifier', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


tests_require = [
    # Pytest needs to come last.
    # https://bitbucket.org/pypa/setuptools/issue/196/
    'pytest',
    'mock',
]


install_requires = [
    'typer',
    'tabulate',
    'tabulate',
    'chardet'
]


# Conditional dependencies:

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        # noinspection PyUnresolvedReferences
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')


# bdist_wheel
extras_require = {
    # https://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
#    'python_version == "3.0" or python_version == "3.1"': ['argparse>=1.2.1'],
}


def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='dateno',
    version=dateno.__version__,
    description=dateno.__doc__.strip(),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/datenoio/datenocmd',
    download_url='https://github.com/datenoio/datenocmd',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    author=dateno.__author__,
    author_email='ivan@begtin.tech',
    license=dateno.__license__,
    entry_points={
        'console_scripts': [
            'dateno = dateno.__main__:main'
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    zip_safe=False,
    keywords='dataset data opendata datasearch',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Data scientists',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
