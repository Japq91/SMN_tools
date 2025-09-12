#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
import numpy as np
import xarray as xr
import os

def extrac_ETA(out_path, gribfile, tipo):
    """
    Extrae variables atmosféricas de un archivo GRIB generado por ETA.
    Variables: precipitación, T2m, HR2m, vientos 10m, vientos en niveles,
               radiación SWdown, presión reducida al nivel del mar.
    Parámetros:
    out_path : str   Carpeta de salida
    gribfile : str   Archivo GRIB (ejemplo: 'latlon_000')
    tipo     : list  Variables a extraer ['pr', 'level_wind', 'mslp', 'wind10m', 't2m', 'r2m', 'ssrd']
    Retorna:
    Archivos NetCDF guardados en la carpeta de salida
    """
    hfp = gribfile[-3:]  # hora file pronóstico
    # --- extraer hora de corrida desde el path ---
    base = os.path.basename(os.path.dirname(gribfile))  # '2025010106'
    init_time = pd.to_datetime(base, format="%Y%m%d%H")

    # --- extraer hora de pronóstico desde el nombre ---
    fname = os.path.basename(gribfile)                  # 'latlon_018'
    m = re.search(r"latlon_(\d+)", fname)
    lead_hours = int(m.group(1)) if m else 0
    valid_time = init_time + pd.to_timedelta(lead_hours, unit="h")

    if 'tp' in tipo:   # Precipitación
        ds = xr.open_dataset(
            gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface', 'shortName': 'tp'}, 'indexpath': ''},
            decode_timedelta=False)
        ds = ds.expand_dims(time=[valid_time])
        ds.to_netcdf(f"{out_path}/tp_{hfp}.nc")

    if 'level_vars' in tipo:   # Viento en niveles isobáricos
        niveles_deseados = [925, 850, 500, 200]
        for var in ['u', 'v']: #agregar aqui nuevas variables en niveles
            ds = xr.open_dataset(
                gribfile, engine="cfgrib",
                backend_kwargs={'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': var}, 'indexpath': ''},
                decode_timedelta=False            )
            ds = ds.expand_dims(time=[valid_time])
            ds.sel(isobaricInhPa=niveles_deseados, method='nearest')\
              .to_netcdf(f"{out_path}/{var}_{hfp}.nc")

    if 'mslp' in tipo:   # Presión al nivel del mar
        ds = xr.open_dataset(
            gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'typeOfLevel': 'meanSea', 'shortName': 'mslet'}, 'indexpath': ''},
            decode_timedelta=False        )
        ds = ds.expand_dims(time=[valid_time])
        ds.to_netcdf(f"{out_path}/mslp_{hfp}.nc")

    elif 'wind10m' in tipo:   # Viento 10m
        for var in ['u', 'v']:
            ds = xr.open_dataset( gribfile, engine="cfgrib",
                    backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10, 'stepType': 'instant' },
                        'indexpath': ''}, decode_timedelta=False)[['%s10'%var]]
            ds = ds.expand_dims(time=[valid_time])
            ds.to_netcdf(f"{out_path}/10{var}_{hfp}.nc")

    if 't2m' in tipo:   # Temperatura 2m
        ds = xr.open_dataset(
            gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2, 'shortName': '2t'}, 'indexpath': ''},
            decode_timedelta=False        )
        ds = ds.expand_dims(time=[valid_time])
        ds.to_netcdf(f"{out_path}/t2m_{hfp}.nc")

    if 'r2m' in tipo:   # Humedad relativa 2m
        ds = xr.open_dataset(
            gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2, 'shortName': '2r'}, 'indexpath': ''},
            decode_timedelta=False        )
        ds = ds.expand_dims(time=[valid_time])
        ds.to_netcdf(f"{out_path}/r2m_{hfp}.nc")
    if 'ssrd' in tipo: # Radiación onda corta (downward shortwave)media
        ds = xr.open_dataset(
            gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface', 'stepType': 'avg','shortName':'avg_sdswrf'}, 'indexpath': ''},
            decode_times=False)
        ds = ds.expand_dims(time=[valid_time])        
        ds.to_netcdf(f"{out_path}/ssrd_{hfp}.nc")

    if len(tipo)==0:  print(f"Tipo '{tipo}' no reconocido")

