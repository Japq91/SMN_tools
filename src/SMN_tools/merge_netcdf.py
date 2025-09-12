#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xarray as xr

def merge_files(list_files, output_file, institution="SENAMHI", source=None):
    """
    Une en un solo NetCDF todas las variables de superficie procesadas previamente.
    Parámetros
    ----------
    list_files : list
        Lista de rutas a NetCDFs de superficie (ya uniformizados con process_netcdf_files).
        Ejemplo: ["sfc_tmp_tp.nc", "sfc_tmp_t2m.nc", "sfc_tmp_sp.nc", ...]
    output_file : str    Nombre del archivo NetCDF de salida con todas las variables unidas.
    """
    # Abrir todos los datasets sin decodificar para consistencia
    datasets = [xr.open_dataset(f, decode_times=True) for f in list_files]

    # Fusionar en un solo dataset
    #combined = xr.merge(datasets)
    #combined = xr.merge(datasets, join="outer")
    combined = xr.merge(datasets, join="outer", compat="override")

    # Agregar metadatos globales
    if source is None:
        # intentar deducir del nombre de salida (ej: wrf_22_sfc.nc → WRF_22)
        base = os.path.basename(output_file)
        source = base.split("_")[1] 

    # Atributos globales reconocidos por CDO
    combined.attrs["institution"] = institution
    combined.attrs["source"] = source
    combined.attrs["history"] = "Generado con SMN_tools"
    combined.attrs["references"] = "https://www.senamhi.gob.pe/"
    combined.attrs["Conventions"] = "CF-1.8"
    #
    # Guardar comprimido
    encoding = {var: {"zlib": True, "complevel": 5} for var in combined.data_vars}
    combined.to_netcdf(output_file, encoding=encoding, format="NETCDF4")
    combined.close()
    print(f"Archivo de superficie generado: {output_file}")

