#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="SMN_tools",
    version="0.1.0",
    description="Herramientas para extraer variables de modelos SENAMHI",
    author="Jonathan apq",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "xarray>=2023.7.0",
        "cfgrib>=0.9.10.4",
        "numpy>=1.24.3",
        "netCDF4>=1.6.2",
        "h5netcdf>=1.2.0",
        "pandas>=2.0.3",
        "eccodes>=2.27.0",
        "h5py>=3.8.0",
        "ipykernel>=6.0.0",
        "matplotlib>=3.7.0",
        "pillow>=9.0.0",
    ],

)
entry_points={
    "console_scripts": [
        "install-smn-kernel=SMN_tools.scripts.install_kernel:main",
    ],
},


