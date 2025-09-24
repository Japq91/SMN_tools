#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

####################################################################################
############# PALETA ############# ############# ############# ############# 
####################################################################################
def get_cmap_norm(variable_name, data_range=None, dataset=None):
    """
    Devuelve cmap y norm según la variable especificada, con soporte para diferentes modelos.
    
    Parámetros:
    variable_name : str
        Nombre de la variable ('prmsl', 'mslet', 't2m', 'tp', 'rh', 'u10', 'v10', etc.)
    data_range : tuple, opcional
        Rango (min, max) de los datos para escalas genéricas
    dataset : netcdf file abierto con xarray, opcional si no se define data_range        
    """

    # =============================
    # Presión a nivel del mar
    # =============================
    if variable_name in ['prmsl', 'mslet']:
        clevs = [978, 981, 984, 987, 990, 993, 996, 999, 1002, 1020, 
                 1023, 1026, 1029, 1032, 1035, 1038, 1041]
        colors = [ 
            (13/255, 71/255, 161/255), (25/255, 135/255, 245/255),
            (30/255, 136/255, 229/255), (21/255, 150/255, 243/255),
            (33/255, 150/255, 243/255), (66/255, 165/255, 245/255),
            (144/255, 202/255, 249/255), (187/255, 222/255, 251/255),
            (255/255, 255/255, 255/255), (255/255, 215/255, 0/255),
            (255/255, 165/255, 0/255), (255/255, 140/255, 0/255),
            (255/255, 69/255, 0/255), (255/255, 0/255, 0/255),
            (220/255, 20/255, 60/255), (178/255, 34/255, 34/255)
        ]
        cmap = mcolors.ListedColormap(colors)
        cmap.set_under((26/255, 35/255, 126/255))
        cmap.set_over((139/255, 0/255, 0/255))
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=len(colors))

    # =============================
    # Temperatura a 2 m
    # =============================
    elif variable_name in ['t2m', 't2']:
        colors = [
            (0/255, 0/255, 128/255),(60/255, 43/255, 153/255),(119/255, 86/255, 178/255),
            (179/255, 129/255, 203/255),(215/255, 151/255, 221/255),(192/255, 119/255, 223/255),
            (170/255, 88/255, 224/255),(148/255, 56/255, 225/255),(138/255, 68/255, 230/255),
            (137/255, 112/255, 236/255),(136/255, 156/255, 243/255),(135/255, 200/255, 249/255),
            (139/255, 216/255, 227/255),(144/255, 229/255, 201/255),(148/255, 241/255, 175/255),
            (156/255, 251/255, 146/255),(184/255, 252/255, 105/255),(211/255, 253/255, 64/255),
            (239/255, 254/255, 23/255),(255/255, 245/255, 0/255),(255/255, 220/255, 0/255),
            (255/255, 196/255, 0/255),(255/255, 172/255, 0/255),(255/255, 133/255, 0/255),
            (255/255, 89/255, 0/255),(255/255, 44/255, 0/255),(255/255, 0/255, 0/255)
        ]
        cmap = LinearSegmentedColormap.from_list('custom_temp', colors)
        clevs = np.linspace(-10, 40, 26)  # puedes ajustar según dataset
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)

    # =============================
    # Precipitación
    # =============================
    elif variable_name in ['tp', 'precip', 'pr']:
        colors = ['#ffffff','#daf9da','#90ee90','#60c960','#30a530','#008000',
                  '#75f4f4','#00ffff','#0adaff','#14b5ff','#1875cf',
                  '#fff6a7','#ffeea2','#ffe59c','#ffdd96','#ffd591',
                  '#ffcc8b','#ffc485','#ffbc80','#ffb37a','#ffab74',
                  '#ffa36f','#ff9a69','#ff9263','#ff8a5e','#ff8158',
                  '#ff7952','#ff714d','#ff6847','#ff6041','#ff583c',
                  '#ff4f36','#ff4730','#ff3f2b','#ff3625','#ff2e1f',
                  '#ff261a','#ff1d14','#ff150e','#ff0d09','#ff0403','#ff0000']
        cmap = ListedColormap(colors)
        clevs = np.linspace(0, 200, len(colors))  # ajusta al rango de precipitación esperado
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)

    # =============================
    # Humedad relativa
    # =============================
    elif variable_name in ['rh', 'hur', 'hurs']:
        colors = [
            (255/255, 192/255, 60/255),
            (255/255, 160/255, 0/255),
            (255/255, 96/255, 0/255),
            (255/255, 50/255, 0/255),
            (225/255, 20/255, 0/255)
        ]
        cmap = LinearSegmentedColormap.from_list('custom_rh', colors)
        clevs = np.arange(0, 101, 20)  # 0 a 100 %
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)

    # =============================
    # Viento a 10 m
    # =============================
    elif variable_name in ['u10', 'v10']:
        clevs = np.arange(0, 30, 2)
        cmap = plt.cm.Blues
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)

    # =============================
    # Configuración genérica
    # =============================
    else:
        if data_range:
            vmin, vmax = data_range
            clevs = np.linspace(vmin, vmax, 20)
        else:
            clevs = np.linspace(np.min(dataset).values, np.max(dataset).values, 11)
            clevs = [int(e) for e in clevs]
        
        cmap = plt.cm.terrain_r
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)
    
    return cmap, norm, clevs

####################################################################################
############# CONTORNO ############# ############# ############# ############# 
####################################################################################

def get_contour(variable_name):
    """
    Devuelve los niveles de contorno específicos para diferentes variables meteorológicas.
    
    Parámetros:
    variable_name : str
        Nombre de la variable meteorológica.
        
    Retorna:
    dict
        Diccionario con configuraciones de contorno para diferentes colores.
    """

    # =============================
    # Presión a nivel del mar
    # =============================
    if variable_name in ['prmsl', 'mslet']:
        return {
            'red':    [1020, 1023, 1026, 1029, 1032, 1035, 1038, 1041],
            'black':  [1005, 1008, 1011, 1014, 1017],
            'blue':   [954, 957, 960, 963, 966, 969, 972, 975,
                       978, 981, 984, 987, 990, 993, 996, 999, 1002]
        }

    # =============================
    # Temperatura a 2m
    # =============================
    elif variable_name in ['t2m', 't2']:
        return {
            'red':      [30, 32, 34, 36, 38, 40],
            'orange':   [25, 26, 27, 28, 29],
            'yellow':   [20, 21, 22, 23, 24],
            'green':    [15, 16, 17, 18, 19],
            'lightblue':[10, 11, 12, 13, 14],
            'blue':     [5, 6, 7, 8, 9],
            'darkblue': [0, 1, 2, 3, 4],
            'purple':   [-5, -4, -3, -2, -1],
            'pink':     [-10, -9, -8, -7, -6]
        }

    # =============================
    # Precipitación acumulada
    # =============================
    elif variable_name in ['tp', 'precip', 'pr']:
        return {
            'blue':    [1, 5, 10],        # lloviznas
            'green':   [20, 30, 40],      # lluvias moderadas
            'yellow':  [50, 75, 100],     # lluvias intensas
            'orange':  [150, 200],        # muy intensas
            'red':     [250, 300, 400]    # extremos
        }

    # =============================
    # Viento a 10m
    # =============================
    elif variable_name in ['u10', 'v10']:
        return {
            'lightblue': [2, 4, 6],
            'blue':      [8, 10, 12],
            'darkblue':  [14, 16, 18],
            'green':     [20, 22, 24],
            'yellow':    [26, 28, 30],
            'orange':    [32, 34, 36],
            'red':       [38, 40, 42]
        }

    # =============================
    # Punto de rocío y humedad relativa
    # =============================
    elif variable_name in ['d2m']:
        # Punto de rocío (°C)
        return {
            'purple':    [-5, -4, -3, -2, -1],
            'blue':      [0, 1, 2, 3, 4],
            'lightblue': [5, 6, 7, 8, 9],
            'green':     [10, 11, 12, 13, 14],
            'lightgreen':[15, 16, 17, 18, 19],
            'yellow':    [20, 21, 22, 23, 24],
            'orange':    [25, 26, 27, 28, 29]
        }

    elif variable_name in ['rh', 'hur', 'hurs', 'r2m']:
        # Humedad relativa (%)
        return {
            'red':       [10, 20, 30],
            'orange':    [40, 50],
            'yellow':    [60, 70],
            'green':     [80, 90],
            'darkgreen': [95, 100]
        }

    # =============================
    # Configuración genérica
    # =============================
    else:
        return {
            'blue': np.linspace(0, 100, 11).tolist()  # 10 intervalos entre 0 y 100
        }

