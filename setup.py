from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in talleyapp1/__init__.py
from talleyapp1 import __version__ as version

setup(
	name="talleyapp1",
	version=version,
	description="A simple application",
	author="Ebuka",
	author_email="ebukaakeru@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
