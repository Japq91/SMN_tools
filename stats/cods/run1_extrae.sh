#!/bin/bash
ruta_actual=$(dirname "$(realpath "$0")") # ruta actual

# #####################################################################
# MODIFICAR en $r_in ---> ruta de los archivos input de SMN_tools
# MODIFICAR en $r0 --->   ruta de los archivos observado y modelo
# ######################################################################

hora=12Z #hora
r_in=/home/jonathan/personal/e4/SMN_tools/data/out/$hora # <----

r0=$(dirname "$ruta_actual") # <----
#r0=../ # <----

mkdir -p $r0/observado $r0/data $r0/recortado $r0/metrics_out $r0/figuras
##########################################################################
# PARTE 1
model=PERU_ETA22
var_name=t2m  #t2m # otras variables extraidas con el paquete SMN_tools
time_prono=3 # numero de dia de prono D1, D2, D3, D4, etc
f_ini=20250224 # datas de inicio formato:  YYYYMMDD
f_fin=20250314 # datas de fin    formato:  YYYMMDD
#
ofile=${model}_D${time_prono}_${f_ini}_${f_fin}_${var_name}.nc
# Ejecutar Python parte 1
python 02_extrae_dias.py $r_in $model $f_ini $f_fin $var_name $time_prono

# PARTE 2
observado=$r0/observado/clima_pisco_t2m.nc # <-----
pronostico=$r0/data/$ofile
observado_cortado=$r0/recortado/$ofile
python 03_extrae_observado.py $observado $pronostico $observado_cortado

# PARTE 3
output_file=$r0/metrics_out/$ofile
python 04_metrics.py $pronostico $observado_cortado $var_name $output_file

# PARTE 4
out_fig=$r0/figuras
python 05_plot.py $output_file $out_fig
