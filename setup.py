#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'Cython==0.23',
    'python-mimeparse==0.1.4',
    'six==1.9.0',
    'SQLAlchemy==1.0.8',
    'wheel==0.24.0',
    'mysql-python'
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='jason',
    version='0.1.0',
    description="Database into JSON API",
    long_description=readme + '\n\n' + history,
    author="Steven Brien",
    author_email='sbrien@hlkagency.com',
    url='https://github.com/spbrien/jason',
    packages=[
        'jason'
    ],
    package_dir={'jason':
                 'jason'},
    entry_points={
        'console_scripts': [
            'jason=jason.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='jason',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
