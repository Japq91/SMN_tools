#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import os
import xarray as xr
import pandas as pd
import sys
#
def cambia_lon(ds):
    if (ds.longitude > 180).any():
        ds = ds.assign_coords(
                longitude=((ds.longitude + 180) % 360) - 180
                ).sortby("longitude")
    return ds


# ================= ENTRADA POR CONSOLA ================= #
if len(sys.argv) != 4:
    print("Uso: python 03_extrae_clima.py <archivo_clima> <archivo_pronostico> <archivo_salida>")
    sys.exit(1)

clima_file = sys.argv[1]
pronostico_file = sys.argv[2]
out_file = sys.argv[3]

# ================= SCRIPT ================= #
# Abrir datasets
ds_clima = xr.open_dataset(clima_file)
ds_clima = cambia_lon(ds_clima)
ds_prono = xr.open_dataset(pronostico_file)


# misma malla
ds_clima = ds_clima.interp(latitude=ds_prono.latitude, longitude=ds_prono.longitude)

# Fechas del pronóstico
fechas_prono = pd.to_datetime(ds_prono.time.values)
dias_prono = fechas_prono.strftime("%m-%d")

# Crear lista para almacenar climatología media de cada fecha
coleccion = []

for i, dia in enumerate(dias_prono):
    
    mask = ds_clima["time"].dt.strftime("%m-%d") == dia
    clima_dia = ds_clima.sel(time=mask)
    
    # Asegurar que quede con la misma fecha que el pronóstico
    fecha_ref = fechas_prono[i]
    clima_dia = clima_dia.assign_coords(time=[fecha_ref])
    
    coleccion.append(clima_dia)

# Concatenar en un solo dataset
clima_final = xr.concat(coleccion, dim="time")

# Guardar
clima_final.to_netcdf(out_file)
print(f"Guardado: {out_file}")

