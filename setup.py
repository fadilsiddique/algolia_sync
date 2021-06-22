# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in algolia_sync/__init__.py
from algolia_sync import __version__ as version

setup(

	name='algolia_sync',
	version=version,
	description='Search',
	author='TRidz',
	author_email='fadil@tridz.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
	
)
