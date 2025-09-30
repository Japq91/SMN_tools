#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr

def filter_dimensions_and_coords(ds, coords_completas, coords_deseadas):
    # Eliminar coordenadas no deseadas del dataset
    for coord in coords_completas[:]:
        if coord not in coords_deseadas:
            # Eliminar la coordenada del dataset
            if coord in ds.coords:
                ds = ds.reset_coords(coord, drop=True)
            # Si hay alguna variable que depende de esa coordenada, también eliminarla
            if coord in ds.data_vars:
                ds = ds.drop_vars(coord)
    
    # Limpiar atributos de coordenadas en todas las variables
    for var_name in ds.data_vars:
        var = ds[var_name]
        # Eliminar atributos que hagan referencia a coordenadas eliminadas
        if 'coordinates' in var.attrs:
            # Filtrar las coordenadas, mantener solo las deseadas
            current_coords = var.attrs['coordinates'].split()
            new_coords = [c for c in current_coords if c in coords_deseadas]
            if new_coords:
                var.attrs['coordinates'] = ' '.join(new_coords)
            else:
                del var.attrs['coordinates']
    
    # Limpiar también atributos globales si existen
    if 'coordinates' in ds.attrs:
        del ds.attrs['coordinates']
    
    return ds
def rename_and_clean(input_file, output_file, var_name_out, dims_out):
    """
    Uniformiza un NetCDF: renombra dimensiones, variables y guarda con compresión.
    ----------
    Parámetros:    
    input_file : str        Ruta del archivo NetCDF de entrada.
    output_file : str        Ruta del archivo NetCDF de salida.
    var_name_out : str        Nombre de la variable principal en el archivo de salida.
    dims_out : list    Lista con los nombres de las dimensiones de salida.
    -------
    Retorna:    xr.Dataset        Dataset transformado y limpio.
    """
    # Abrir dataset
    ds = xr.open_dataset(input_file, decode_times=True, decode_timedelta=False)

    # Detectar variable principal
    var_in = [v for v in ds.data_vars][0]
    da = ds[var_in]    
    dims_in = list(da.dims) # Dimensiones originales
    
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
    #da_new.attrs.update(ds.attrs)
    #
    coords_ori = list(ds.coords.keys())  # ['time', 'step', 'heightAboveGround', 'latitude', 'longitude', 'valid_time']
    #print(coords_ori)
    da_new=filter_dimensions_and_coords(da_new,coords_ori,dims_out)

    return da_new

