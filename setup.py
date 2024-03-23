from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in site_monitor/__init__.py
from site_monitor import __version__ as version

setup(
	name="site_monitor",
	version=version,
	description="Monitors the stats of sites and servers",
	author="Ebuka Akeru",
	author_email="ebukaakeru@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
