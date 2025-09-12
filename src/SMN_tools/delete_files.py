#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def clean_outdir(outdir: str):
    """
    Elimina todos los archivos .nc dentro de un directorio de salida.
    Parámetros
    ----------
    outdir : str        Ruta de la carpeta donde se eliminarán los NetCDF.
    """
    if not os.path.exists(outdir):
        return
    for f in os.listdir(outdir):
        if f.endswith(".nc"):
            file_path = os.path.join(outdir, f)
            try:
                os.remove(file_path)
                print(f"Eliminado: {file_path}")
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")
