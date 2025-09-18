#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
####################################################################################
def get_cmap_norm(variable_name, data_range=None, model_type=None):
    """
    Devuelve cmap y norm según la variable especificada, con soporte para diferentes modelos.
    
    Parámetros:
    variable_name : str
        Nombre de la variable ('prmsl', 'mslet', 't2m', 'u10m', etc.)
    data_range : tuple, opcional
        Rango (min, max) de los datos para escalas genéricas
    model_type : str, opcional
        Tipo de modelo ('gfs', 'wrf', 'eta') para ajustes específicos
    """
    # Configuración para presión al nivel del mar (común a todos los modelos)
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
        
    # Configuración para temperatura a 2m
    elif variable_name in ['t2m']:
        clevs = np.arange(-10, 40, 2)
        cmap = plt.cm.coolwarm
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)
        
    # Configuración para viento a 10m
    elif variable_name in ['u10', 'v10']:
        clevs = np.arange(0, 30, 2)
        cmap = plt.cm.Blues
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)
        
    # Configuración para humedad
    elif variable_name in ['d2m', 'rh']:
        clevs = np.arange(0, 100, 10)
        cmap = plt.cm.YlGnBu
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)
    
    else:
        # Configuración genérica para otras variables
        if data_range:
            vmin, vmax = data_range
            clevs = np.linspace(vmin, vmax, 20)
        else:
            clevs = np.linspace(np.min(data), np.max(data), 20)
        
        cmap = plt.cm.viridis
        norm = mcolors.BoundaryNorm(boundaries=clevs, ncolors=cmap.N)
    
    return cmap, norm, clevs

####################################################################################
def get_contour(variable_name):
    """
    Devuelve los niveles de contorno específicos para diferentes variables meteorológicas
    
    Parámetros:
    variable_name : str
        Nombre de la variable meteorológica
        
    Retorna:
    dict
        Diccionario con configuraciones de contorno para diferentes colores
    """
    if variable_name in ['prmsl', 'mslet']:
        return {
            'red': [1020, 1023, 1026, 1029, 1032, 1035, 1038, 1041],
            'black': [1005, 1008, 1011, 1014, 1017],
            'blue': [954, 957, 960, 963, 966, 969, 972, 975, 978, 981, 984, 987, 990, 993, 996, 999, 1002]
        }
    
    elif variable_name == 't2m':
        # Contornos para temperatura a 2m (°C)
        return {
            'red': [30, 32, 34, 36, 38, 40],
            'orange': [25, 26, 27, 28, 29],
            'yellow': [20, 21, 22, 23, 24],
            'green': [15, 16, 17, 18, 19],
            'lightblue': [10, 11, 12, 13, 14],
            'blue': [5, 6, 7, 8, 9],
            'darkblue': [0, 1, 2, 3, 4],
            'purple': [-5, -4, -3, -2, -1],
            'pink': [-10, -9, -8, -7, -6]
        }
    
    elif variable_name in ['u10m', 'v10m', 'wind10m']:
        # Contornos para velocidad del viento a 10m (m/s)
        return {
            'lightblue': [2, 4, 6],
            'blue': [8, 10, 12],
            'darkblue': [14, 16, 18],
            'green': [20, 22, 24],
            'yellow': [26, 28, 30],
            'orange': [32, 34, 36],
            'red': [38, 40, 42]
        }
    
    elif variable_name in ['d2m', 'rh']:
        # Contornos para punto de rocío (d2m en °C) o humedad relativa (rh en %)
        if variable_name == 'd2m':
            return {
                'purple': [-5, -4, -3, -2, -1],
                'blue': [0, 1, 2, 3, 4],
                'lightblue': [5, 6, 7, 8, 9],
                'green': [10, 11, 12, 13, 14],
                'lightgreen': [15, 16, 17, 18, 19],
                'yellow': [20, 21, 22, 23, 24],
                'orange': [25, 26, 27, 28, 29]
            }
        else:  # rh - humedad relativa
            return {
                'red': [10, 20, 30],
                'orange': [40, 50],
                'yellow': [60, 70],
                'green': [80, 90],
                'darkgreen': [95, 100]
            }
    
    else:
        # Configuración genérica para variables no especificadas
        return {
            'blue': np.linspace(0, 100, 11).tolist()  # 10 intervalos entre 0 y 100
        }
