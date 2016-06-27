#!/usr/bin/env python
from setuptools import setup, find_packages


bitnfly_dev = {'develop': [
    "pep8-naming>=0.3.3",   # MIT license
    "flake8>=2.5.1",        # MIT license
    "pyflakes>=1.0.0",      # MIT license
    "coverage",
    ]
}

setup(
    name='bitnfly',
    version='0.0.4',
    description='BitnFly is a mini API for working with bit flags',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/bitnfly',
    packages=find_packages(),
    test_suite='BitnFly.tests',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    extras_require=bitnfly_dev
)