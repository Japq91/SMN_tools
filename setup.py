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
        "xarray",
        "numpy",
        "netCDF4",
        "cfgrib",
        "h5netcdf",
        "ipykernel",   # <-- aquí
    ],
)
entry_points={
    "console_scripts": [
        "install-smn-kernel=SMN_tools.scripts.install_kernel:main",
    ],
},


