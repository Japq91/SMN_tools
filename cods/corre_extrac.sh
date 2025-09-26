#!/bin/bash
################## RUTAS ######################
r0=/scratch/Datatemporal/SMN/data/regional # Ruta de datos iniciales por modelo
outdir=/scratch/SMN_tools/out # Ruta donde se genera la extraccion
#
hora=12 #00 #12
model="PERU_ETA22"  #"PERU_WRF22"
meses=(02 03) #(01 02 03) # meses a procesar
anio=2025 # Año


##########################################################################
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
	echo "##############################"
        echo model: "$model" 
	echo fecha: "$fecha" 
	echo horas: "$hora"Z
	python corre_extrac.py $r0 $model $fecha $hora $outdir

    done
done
