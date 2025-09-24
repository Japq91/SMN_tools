#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from glob import glob as gb
import xarray as xr
import sys
import numpy as np
#
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
# ================= FUNCIONES ================= #
def escalar_diario(da, var_name, tz_offset= -5):
    """ Ajusta de UTC a hora local (GTM-5) y luego escala a diario.
    Para precipitación: acumulado de 07 a 07 según normativa OMM. 
    Para otras variables: promedio diario local.  """
    # Ajustar tiempo: convertir UTC a hora local (desplazar tz_offset horas)
    da = da.assign_coords(time=da.time + np.timedelta64(tz_offset, "h"))
    if var_name == "tp":
        # Acumulado 07:00 → 07:00 del día siguiente
        da = da.assign_coords(time=da.time - np.timedelta64(7, "h"))
        return da.resample(time="1D").sum()
    else:
        # Para otras variables: promedio diario normal
        return da.resample(time="1D").mean()

def extraer_dia(ds, var_name, day_index):
    """Escala diaria y extrae un día específico (D1, D2...)."""
    da = escalar_diario(ds[var_name], var_name)
    return da.isel(time=day_index - 1)  # D1 = índice 0
 
def cambia_lon(ds_prono):
    if (ds_prono.longitude > 180).any():
        ds_prono = ds_prono.assign_coords(
                longitude=((ds_prono.longitude + 180) % 360) - 180
                ).sortby("longitude")
    return ds_prono

# ================= ENTRADA POR CONSOLA ================= #
if len(sys.argv) != 7:
    print("Uso: python 02_extrae_dias.py <input_dir> <fecha_ini:YYYYMM> <fecha_fin:YYYYMM> <var_name> <day> <modelo>")
    print("Ejemplo: python 02_extrae_dias.py /home/jonathan/.../out 202502 202503 t2m 3 PERU_ETA22")
    sys.exit(1)

input_dir = sys.argv[1]
modelo = sys.argv[2]
fecha_ini = sys.argv[3]
fecha_fin = sys.argv[4]
var_name = sys.argv[5]
day_index = int(sys.argv[6])

# ================= BUSCAR ARCHIVOS ================= #
archivos = sorted(gb(f"{input_dir}/*.nc"))
if not archivos:
    raise FileNotFoundError(f"No se encontraron archivos en {input_dir}")

# Filtrar archivos en rango de fechas
archivos_filtrados = []
for archivo in archivos:
    base = os.path.basename(archivo)
    partes = base.split("_")
    if len(partes) < 3:
        continue
    fecha_hora = partes[-2]  # asume formato MODELO_YYYYMMDDHH_tipo.nc
    if fecha_ini <= fecha_hora[:8] <= fecha_fin:
        archivos_filtrados.append(archivo)

if not archivos_filtrados:
    raise FileNotFoundError(f"No se encontraron archivos entre {fecha_ini} y {fecha_fin} en {input_dir}")

# ================= SCRIPT PRINCIPAL ================= #

output_dir = f"{PARENT_DIR}/data"
os.makedirs(output_dir, exist_ok=True)

coleccion = []
for archivo in archivos_filtrados:
    print(f"Procesando {archivo} (D{day_index}) ...")
    with xr.open_dataset(archivo) as ds:
        var_dia = extraer_dia(ds, var_name, day_index)
        coleccion.append(var_dia)

nombre_salida = f"{modelo}_D{day_index}_{fecha_ini}_{fecha_fin}_{var_name}.nc"
print(nombre_salida)

#'''
# Concatenar en dimensión tiempo
serie = xr.concat(coleccion, dim="time")
serie = cambia_lon(serie)
# Nombre de salida solicitado
ruta_salida = os.path.join(output_dir, nombre_salida)
serie.to_netcdf(ruta_salida)
print(f"Guardado: {ruta_salida}")
# '''
