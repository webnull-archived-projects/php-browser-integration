#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from distutils.core import setup

setup(
    name='phpBrowserIntegration',
    author='Damian Kęska',
    license = "LGPLv3",
    package_dir={'': 'src'},
    packages=['phpBrowserIntegration'],
    author_email='webnull.www@gmail.com',
    scripts=['php-browser-integration'],
    install_requires=[
        'pantheradesktop', 'tornado'
    ]
)