#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
import numpy as np
import xarray as xr
import os
#
import numpy as np
import xarray as xr

def make_structured(dataset, var_name, coord_lat='latitude', coord_lon='longitude', coord_z=None):
    """
    Reorganiza un dataset para que las coordenadas de latitud y longitud sean únicas. 
    Si la variable contiene una dimensión vertical (e.g., presión), la reorganiza en 3D (z, lat, lon). 
    Si no, en 2D (lat, lon).
    
    También se asegura de que las coordenadas de tiempo (time) y tiempo válido (valid_time) se incluyan.
    
    Parámetros
    ----------
    dataset : xr.Dataset
        Dataset que contiene la variable a reorganizar.
    var_name : str
        Nombre de la variable dentro del dataset a reorganizar.
    coord_lat : str, opcional
        Nombre de la coordenada de latitud (default: 'latitude').
    coord_lon : str, opcional
        Nombre de la coordenada de longitud (default: 'longitude').
    coord_z : str, opcional
        Nombre de la coordenada vertical (e.g., presión). Si no se proporciona, se reorganiza en 2D.
    
    Retorna
    -------
    xr.Dataset
        Dataset reorganizado con coordenadas únicas de latitud y longitud. 
        En 3D si hay un eje z, en 2D si no.
    """

    # Coordenadas únicas
    lat_unicas = np.unique(dataset[coord_lat].values)
    lon_unicas = np.unique(dataset[coord_lon].values)

    # Extraer datos base
    var = dataset[var_name].values
    coords = {coord_lat: lat_unicas, coord_lon: lon_unicas}

    # Determinar forma esperada y dimensiones
    if coord_z and coord_z in dataset.coords:
        dims = [coord_z, coord_lat, coord_lon]
        shape = (dataset.sizes[coord_z], len(lat_unicas), len(lon_unicas))
        coords[coord_z] = dataset[coord_z].values
    else:
        dims = [coord_lat, coord_lon]
        shape = (len(lat_unicas), len(lon_unicas))

    # Reorganizar variable
    var_reshaped = var.reshape(shape)

    # Construir nuevo dataset
    nuevo_dataset = xr.Dataset({var_name: (dims, var_reshaped)}, coords=coords)

    # Mantener coordenadas de tiempo si existen
    for t_coord in ['time', 'valid_time']:
        if t_coord in dataset.coords:
            nuevo_dataset = nuevo_dataset.assign_coords({t_coord: dataset[t_coord].values})

    return nuevo_dataset

#
def extrac_WRF(out_path, gribfile, tipo):
    """
    Extrae variables atmosféricas de un archivo GRIB generado por WR.
    Variables disponibles:
      - 'pr'          : precipitación acumulada (tp, superficie)
      - 'level_wind'  : vientos U y V en niveles isobáricos
      - 'level_temp'  : temperatura en niveles isobáricos
      - 'level_hum'   : humedad relativa en niveles isobáricos
      - 'level_gh'    : geopotencial en niveles isobáricos
      - 'mslp'        : presión reducida al nivel del mar
      - 'wind10m'     : viento a 10 m (10u, 10v)
      - 't2m'         : temperatura a 2 m
      - 'd2m'         : dew point a 2 m
      - 'r2m'         : humedad relativa a 2 m
    Parámetros:
    -----------
    out_path : str        Carpeta de salida
    gribfile : str        Archivo GRIB (ejemplo: 'WRFPRS_d01.00')
    tipo : list        Variables a extraer. Ejemplo: ['pr','wind10m','t2m']
    """

    hfp0 = gribfile.split('.')[-1]  # último par de dígitos como paso (ej: 00, 06, 12)
    hfp = '%03d'%int(hfp0) 
    base = os.path.basename(os.path.dirname(gribfile))
    try:        init_time = pd.to_datetime(base, format="%Y%m%d%H")
    except Exception:        init_time = None

    m = re.search(r"\.(\d+)$", gribfile)
    lead_hours = int(m.group(1)) if m else 0
    valid_time = init_time + pd.to_timedelta(lead_hours, unit="h") if init_time else None

    # --- Precipitación acumulada ---
    if 'tp' in tipo:
        ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName':'tp','typeOfLevel':'surface'}, 'indexpath': ''},
            decode_timedelta=False)
        if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
        ds = make_structured(ds, var_name=list(ds.data_vars)[0])
        ds.to_netcdf(f"{out_path}/tp_{hfp}.nc")

    # --- Variables en niveles ---
    if 'level_vars' in tipo:
        niveles_deseados = [925, 850, 500, 200]
        for var in ['u','v']: #agregar aqui en caso nuevas variavles de niveles ['u','v','t','r','gh']
            ds = xr.open_dataset(gribfile, engine="cfgrib",
                backend_kwargs={'filter_by_keys': {'shortName': var, 'typeOfLevel':'isobaricInhPa'}, 'indexpath': ''},
                decode_timedelta=False)
            if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
            ds = make_structured(ds, var_name=list(ds.data_vars)[0], coord_z='isobaricInhPa')
            ds.sel(isobaricInhPa=niveles_deseados, method='nearest')\
              .to_netcdf(f"{out_path}/{var}_{hfp}.nc")

    # --- MSLP ---
    if 'mslp' in tipo:
        ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName':'mslet','typeOfLevel':'meanSea'}, 'indexpath': ''},
            decode_timedelta=False)
        if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
        ds = make_structured(ds, var_name=list(ds.data_vars)[0])
        ds.to_netcdf(f"{out_path}/mslp_{hfp}.nc")

    # --- Viento 10m ---
    if 'wind10m' in tipo:
        for var in ['10u','10v']:
            ds = xr.open_dataset(gribfile, engine="cfgrib",
                backend_kwargs={'filter_by_keys': {'shortName': var, 'typeOfLevel':'heightAboveGround','level':10}, 'indexpath': ''},
                decode_timedelta=False)
            if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
            ds = make_structured(ds, var_name=list(ds.data_vars)[0])
            ds.to_netcdf(f"{out_path}/{var}_{hfp}.nc")

    # --- Temperatura 2m ---
    if 't2m' in tipo:
        ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName':'2t','typeOfLevel':'heightAboveGround','level':2}, 'indexpath': ''},
            decode_timedelta=False)
        if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
        ds = make_structured(ds, var_name=list(ds.data_vars)[0])
        ds.to_netcdf(f"{out_path}/t2m_{hfp}.nc")

    # --- Dew Point 2m ---
    if 'd2m' in tipo:
        ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName':'2d','typeOfLevel':'heightAboveGround','level':2}, 'indexpath': ''},
            decode_timedelta=False)
        if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
        ds = make_structured(ds, var_name=list(ds.data_vars)[0])
        ds.to_netcdf(f"{out_path}/d2m_{hfp}.nc")

    # --- Humedad relativa 2m ---
    if 'r2m' in tipo:
        ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName':'2r','typeOfLevel':'heightAboveGround','level':2}, 'indexpath': ''},
            decode_timedelta=False)
        if valid_time is not None: ds = ds.expand_dims(time=[valid_time])
        ds = make_structured(ds, var_name=list(ds.data_vars)[0])
        ds.to_netcdf(f"{out_path}/r2m_{hfp}.nc")

    if len(tipo)==0:        print(f"Tipo '{tipo}' no reconocido")

