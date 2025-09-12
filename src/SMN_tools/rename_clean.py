#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr

def rename_and_clean(input_file, output_file, var_name_out, dims_out):
    """
    Uniformiza un NetCDF: renombra dimensiones, variables y guarda con compresión.
    Parámetros
    ----------
    input_file : str        Ruta del archivo NetCDF de entrada.
    output_file : str        Ruta del archivo NetCDF de salida.
    var_name_out : str        Nombre de la variable principal en el archivo de salida.
    dims_out : list    Lista con los nombres de las dimensiones de salida.
        Ejemplos:
            ['time', 'lat', 'lon']                -> superficie
            ['time', 'lev', 'lat', 'lon']         -> niveles
    Retorna
    -------
    xr.Dataset        Dataset transformado y limpio.
    """
    # Abrir dataset
    ds = xr.open_dataset(input_file, decode_times=True, decode_timedelta=False)
    # Detectar variable principal
    var_in = [v for v in ds.data_vars][0]
    da = ds[var_in]
    # Dimensiones originales
    dims_in = list(da.dims)
    # Si existe "time" en coords pero no en dims (ej. 1 archivo = 1 tiempo)
    if "time" in ds.coords and "time" not in dims_in:
        da = da.expand_dims("time")          # añade eje tiempo
        da = da.transpose("time", *dims_in)  # asegura orden
        dims_in = ["time"] + dims_in

    # Validar dimensiones
    if len(dims_in) != len(dims_out):
        raise ValueError( f"Número de dimensiones no coincide: entrada {dims_in}, salida {dims_out}" )

    # Mapear dims → nuevas dims
    rename_dict = dict(zip(dims_in, dims_out))
    da_new = da.rename(rename_dict).to_dataset(name=var_name_out)

    # Asignar coordenadas de tiempo si existen
    if "time" in ds.coords:
        da_new = da_new.assign_coords(time=ds["time"].values)
        da_new["time"].attrs.update(ds["time"].attrs)

    # Copiar atributos globales
    da_new.attrs.update(ds.attrs)

    # Eliminar coords innecesarias
    for extra in ["valid_time", "step", "forecast_reference_time"]:
        if extra in da_new.coords:
            da_new = da_new.drop_vars(extra)

    # Configurar compresión
    encoding = {var_name_out: {"zlib": True, "complevel": 5}}

    # Guardar (opcional, si quieres escribir directo)
    # da_new.to_netcdf(output_file, format="NETCDF4", encoding=encoding)

    return da_new


