#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import xarray as xr
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <archivo_netcdf> <ruta_salida>")
        sys.exit(1)
    else: 
        print('plotea')
    # Argumentos
    nc_file = sys.argv[1]
    output_dir = sys.argv[2]
    # Extraer solo el nombre del archivo sin ruta
    file_name = os.path.basename(nc_file)
    # Abrir dataset
    ds = xr.open_dataset(nc_file)
    variables_lista=[e for e in list(ds.variables) if not e in ['latitude','longitude']]
    # Iterar sobre variables (excluyendo coordenadas típicas)
    for varia in variables_lista:
        print(f"Generando figura para {varia}...")

        plt.figure()
        ds[varia].plot(robust=True, extend='both', levels=11)
        plt.title(f"{file_name}\n{varia}")

        # Guardar figura
        out_path = os.path.join(output_dir, f"{varia}_{file_name}")
        plt.savefig('%s.png'%out_path[:-3], dpi=100, bbox_inches="tight")
        plt.close()

    print(f"Figuras guardadas en: {output_dir}")

if __name__ == "__main__":
    main()

