#!/usr/bin/env python3
from setuptools import setup

setup(
    name='OneSky Sync',
    author='Elvanto',
    packages=[
        'onesky_sync',
        'onesky_sync.authentication',
        'onesky_sync.cli',
        'onesky_sync.json_sync',
        'onesky_sync.sync',
        'onesky_sync.upload',
    ],
    author_email='support@elvanto.com',
    version='2.0.3',
    entry_points={
        'console_scripts': [
            'onesky-sync=onesky_sync.cli.main:main',
        ]
    },
    install_requires=[
        'requests',
        'polib'
    ]
)
