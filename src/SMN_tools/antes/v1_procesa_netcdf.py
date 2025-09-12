#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xarray as xr
from .rename_clean import rename_and_clean

def process_netcdf_files(list_files, prefix_out, new_dims):
    datasets = []
    for file in list_files:
        var_name = os.path.basename(file).split("_")[0]
        ds = xr.open_dataset(file, decode_times=True,decode_timedelta=False)
        
        # Usar la función externa
        ds = rename_and_clean(ds, new_dims)

        # Renombrar variable principal
        if len(ds.data_vars) == 1:
            old_var = list(ds.data_vars)[0]
            ds = ds.rename({old_var: var_name})
        else:
            raise ValueError(f"El archivo {file} tiene más de una variable, se esperaba solo una.")

        datasets.append(ds)

    # Concatenar en el tiempo
    time_dim = new_dims[0]
    combined = xr.concat(datasets, dim=time_dim)

    # Nombre de salida dinámico
    var_name_out = list(combined.data_vars.keys())[0]
    out_dir = os.path.dirname(list_files[0])
    out_file = os.path.join(out_dir, f"{prefix_out}_tmp_{var_name_out}.nc")

    # Guardar comprimido
    encoding = {var: {"zlib": True, "complevel": 5} for var in combined.data_vars}
    combined.to_netcdf(out_file, encoding=encoding)

    print(f"Archivo generado: {out_file}")


# ================================
# Ejemplo de uso:
# files = ["10u_006.nc", "10u_009.nc", "10u_012.nc"]
# new_dims = ["new_time", "new_lat", "new_lon", "new_level"]
# process_netcdf_files(files, prefix_out="sfc", new_dims=["new_time", "new_lat", "new_lon"])
