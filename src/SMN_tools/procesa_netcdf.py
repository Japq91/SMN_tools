#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import xarray as xr
from .rename_clean import rename_and_clean
def process_netcdf_files(list_files, prefix_out, new_dims):
    """
    Une varios archivos NetCDF, renombra dimensiones/variables con ayuda de rename_and_clean,
    elimina coords extra, añade metadatos CF y guarda comprimido.
    Parámetros
    ----------
    list_files : list        Lista de rutas a archivos NetCDF, ej: ["10u_006.nc", "10u_009.nc", ...]
    prefix_out : str        Prefijo para el archivo de salida (ej. "sfc", "prs").
    new_dims : list        Lista con los nuevos nombres de dimensiones.        
    """
    datasets = []
    for file in list_files:
        # nombre de la variable a partir del archivo
        var_name = os.path.basename(file).split("_")[0]
        # archivo temporal de salida intermedio (no se usará en disco, pero requerido por la interfaz)
        tmp_out = os.path.join(os.path.dirname(file), f"tmp_{var_name}.nc")
        # usar rename_and_clean
        ds = rename_and_clean(file, tmp_out, var_name, new_dims)
        print("#" * 10)
        datasets.append(ds)
        #print(ds)
        

    # concatenar en la dimensión de tiempo
    time_dim = new_dims[0]
    #combined = xr.concat(datasets, dim=time_dim)
    #combined = xr.concat(datasets, dim=time_dim, coords="minimal")
    combined = xr.concat(datasets, dim=time_dim, coords="minimal", compat="override")  
    combined = combined.sortby("time", ascending=True)
    # añadir metadatos CF mínimos
    combined[time_dim].attrs.update({"standard_name": "time", "long_name": "time"})
    if "latitude" in new_dims:
        combined["latitude"].attrs.update({"standard_name": "latitude", "units": "degrees_north"})
    if "longitude" in new_dims:
        combined["longitude"].attrs.update({"standard_name": "longitude", "units": "degrees_east"})
    if "isobaricInhPa" in new_dims:
        combined["isobaricInhPa"].attrs.update({"standard_name": "air_pressure", "units": "hPa"})

    # nombre de salida dinámico
    var_name_out = list(combined.data_vars.keys())[0]
    out_dir = os.path.dirname(list_files[0])
    out_file = os.path.join(out_dir, f"{prefix_out}_tmp_{var_name_out}.nc")

    # guardar comprimido con zlib
    encoding = {var: {"zlib": True, "complevel": 5} for var in combined.data_vars}
    combined.to_netcdf(out_file, encoding=encoding, format="NETCDF4")
    print(f"Archivo generado: {out_file}")

