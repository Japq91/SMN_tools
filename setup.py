from setuptools import setup, find_packages

setup(
    name="SMN_tools",
    version="0.1.0",
    description="Herramientas para extraer variables de modelos SENAMHI",
    author="Jonathan apq",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "xarray",
        "cfgrib",
        "numpy",
        "netCDF4",
        "h5netcdf"
        ],

    python_requires=">=3.9",
)

