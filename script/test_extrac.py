#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import xarray as xr
from SMN_tools import extrac_ETA
from SMN_tools import extrac_WRF
from SMN_tools import process_netcdf_files
from SMN_tools import merge_files
from SMN_tools import clean_outdir
from glob import glob as gb

# --- FORZAR CARPETA -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(BASE_DIR, "../cfgrib_cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ["GRIB_INDEX_DIR"] = cache_dir
#

#r0 = '/scratch/Datatemporal/SMN/data/regional' # Ruta de datos iniciales por modelo
r0 = '/home/jonathan/personal/e4/SMN_tools/data'
#
model = "PERU_WRF22" # "PERU_WRF22" #"PERU_ETA22" #"PERU_WRF22"
hor = "06"
dia = "01"
mes = "01"
yea = "2025"
#
#outdir = "/scratch/SMN_tools/out/%s"%model
outdir = '%s/out/%s'%(r0,model)
os.system('mkdir -p %s'%outdir)
clean_outdir(outdir)

##########################################################################

if "ETA" in model: 
    grib = f'{r0}/{model}/{yea}/{yea}{mes}/{yea}{mes}{dia}{hor}'
    files_pro=gb('%s/latlon_*'%grib)
elif "WRF" in model: 
    grib = f'{r0}/{model}/{yea}{mes}/{yea}{mes}{dia}{hor}'
    files_pro=gb('%s/WRFPRS_*'%grib)
else: print('model GFS??')
#
files_prono = [e for e in sorted(files_pro) if not any(x in e for x in ['idx', 'ctl'])] 
print(files_prono)
tipos = ['tp','level_vars','wind10m','t2m','r2m','ssrd','mslp'][:]
print(tipos)

##################### EXTRAE VARIABLES ############################
for file_p in files_prono[:]:
    print(file_p)
    if "ETA" in model: extrac_ETA(outdir, file_p, tipos)
    if "WRF" in model: extrac_WRF(outdir, file_p, tipos)
#'''

#################### MODIFICA COORDENADAS Y MERGE TIME ###########
#'''
for var_in in ['prs','sfc'][:]: # condiciona para variables de superficie o de altura
    if 'prs' in var_in: 
        nueva_lista= ['u','v']  #modifica si quiere agregar + variables en niveles
        new_dims0=["time", "lev","lat", "lon"]
    else:
        lista_filtrada = [elemento for elemento in tipos if elemento != 'level_vars']
        nueva_lista = []
        for elemento in lista_filtrada:
            if elemento == 'wind10m': nueva_lista.extend(['10u', '10v'])            
            else: nueva_lista.append(elemento)
        new_dims0=["time", "lat", "lon"]
    print('\n',nueva_lista,'**'*40)
    for var in nueva_lista[:]: #modifica aqui para todas las variables        
        files_vars=gb('%s/%s_*'%(outdir,var))
        if len(files_vars)==0: print('Sin Archivos para variable: %s'%var); continue
        print('#'*20,var,'#'*20)
        process_netcdf_files(files_vars, prefix_out=var_in, new_dims=new_dims0)
#'''

#################### MERGE VARIABLES ###########

# Crear carpeta de la corrida 
run_dir = os.path.join(os.path.dirname(outdir), f"{hor}Z")
os.makedirs(run_dir, exist_ok=True)

# Fecha y hora del run
fecha_hor = f"{yea}{mes}{dia}{hor}"

for var_in in ['prs', 'sfc'][:]:
    files_variables = gb(f"{outdir}/{var_in}_*")
    if len(files_variables) == 0:
        print(f"Sin archivos para {var_in}, no se puede hacer merge.")
        continue

    # Construir nombre final según formato solicitado
    final_name = f"{model}_{fecha_hor}_{var_in}.nc"
    out_file = os.path.join(run_dir, final_name)

    print(f"Generando archivo final: {out_file}")
    merge_files(files_variables, out_file)

