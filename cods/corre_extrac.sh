#!/bin/bash

#########################################################
################## E D I T A B L E ######################

# MODELOS: PERU_ETA22, PERU_WRF22, SUDAMERICA_ETA32, SUDAMERICA_WRF33, NPE5k_WRF, ETA10km, NCN1k_WRF
hora=12 #00 #12
model="PERU_ETA22"
meses=(02 03) #(01 02 03) # meses a procesar
anio=2025 # Año
outdir=/scratch/SMN_tools/out # extraccion ruta

# condicional segun modelo
if [ "$model" = "PERU_ETA22" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model/$anio
elif [ "$model" = "SUDAMERICA_ETA32" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model/$anio
elif [ "$model" = "PERU_WRF22" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model
elif [ "$model" = "SUDAMERICA_WRF33" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model
elif [ "$model" = "NPE5k_WRF" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model/grib2
elif [ "$model" = "ETA10km" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model
elif [ "$model" = "NCN1k_WRF" ]; then
  r0=/scratch/Datatemporal/SMN/data/regional/$model/grib2
else # agregar otros modelos
  echo "Error: Modelo no reconocido: $model"
  exit 1
fi
################# F I N -- E D I T ######################
#########################################################

for mes in "${meses[@]}"; do    
  case $mes in #Determinar el número de días del mes
    01|03|05|07|08|10|12) dias=31 ;;
    04|06|09|11) dias=30 ;;
    02) 
    # Febrero: verificar si es año bisiesto
    if (( anio % 4 == 0 && ( anio % 100 != 0 || anio % 400 == 0 ) )); then dias=29
    else dias=28; fi;;
  esac    
  # Generar los días del mes
  for dia in $(seq -w 1 $dias); do
    fecha="$anio$mes$dia"
    input_path="$r0/$anio$mes/${fecha}${hora}"
    echo "##############################"
    echo model: "$model" 
    echo fecha: "$fecha" horas: "$hora"Z
    echo Ruta input "$input_path"
    if [ ! -d "$input_path" ]; then
      echo "ADVERTENCIA: Directorio no encontrado: $input_path"
      continue
    fi
    python corre_extrac.py $input_path $model $fecha $hora $outdir
  done
done
