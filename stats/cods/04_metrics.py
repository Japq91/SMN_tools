#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr
import numpy as np
import sys

# ================= FUNCIONES ================= #

def rmse(observations, forecasts, time_dim="time"):
    return np.sqrt(((forecasts - observations) ** 2).mean(dim=time_dim))

def bias(observations, forecasts, time_dim="time"):
    return forecasts.mean(dim=time_dim) - observations.mean(dim=time_dim)

def pearson_correlation(observations, forecasts, time_dim="time"):
    obs_mean = observations.mean(dim=time_dim)
    fcst_mean = forecasts.mean(dim=time_dim)
    numerator = ((forecasts - fcst_mean) * (observations - obs_mean)).sum(dim=time_dim)
    denominator = np.sqrt(((forecasts - fcst_mean) ** 2).sum(dim=time_dim) *
                          ((observations - obs_mean) ** 2).sum(dim=time_dim))
    return xr.where(denominator > 0, numerator / denominator, np.nan)

def index_of_agreement(observations, forecasts, time_dim="time"):
    obs_mean = observations.mean(dim=time_dim)
    numerator = ((forecasts - observations) ** 2).sum(dim=time_dim)
    term1 = np.abs(forecasts - obs_mean)
    term2 = np.abs(observations - obs_mean)
    denominator = ((term1 + term2) ** 2).sum(dim=time_dim)
    return xr.where(denominator > 0, 1 - (numerator / denominator), np.nan)

def nse(observations, forecasts, time_dim="time"):
    numerator = ((observations - forecasts) ** 2).sum(dim=time_dim)
    denominator = ((observations - observations.mean(dim=time_dim)) ** 2).sum(dim=time_dim)
    return 1 - (numerator / denominator)

def kge(observations, forecasts, time_dim="time"):
    r = pearson_correlation(observations, forecasts, time_dim)
    alpha = forecasts.std(dim=time_dim) / observations.std(dim=time_dim)
    beta = forecasts.mean(dim=time_dim) / observations.mean(dim=time_dim)
    return 1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)

def accuracy_within_sigma(observations, forecasts, time_dim="time", k=1.0):
    std_obs = observations.std(dim=time_dim)
    lower = observations - k * std_obs
    upper = observations + k * std_obs
    ok = (forecasts >= lower) & (forecasts <= upper)
    return ok.sum(dim=time_dim) / ok.sizes[time_dim]

# ================= SCRIPT PRINCIPAL ================= #
if len(sys.argv) != 5:
    print("Uso: python metrics.py <forecast_file> <obs_file> <var_name> <output_file>")
    sys.exit(1)

forecast_file = sys.argv[1]
obs_file = sys.argv[2]
var_name = sys.argv[3]
output_file = sys.argv[4]

# Abrir archivos
ds_fcst = xr.open_dataset(forecast_file)
#print(ds_fcst)
ds_obs = xr.open_dataset(obs_file)
#print(ds_obs)

#
obs = ds_obs[var_name]
fcst = ds_fcst[var_name]

if 't2m' in var_name: 
    fcst = ds_fcst[var_name]-273.15
elif 'prmsl' in var_name: 
    fcst = ds_fcst[var_name]/100
else: 
    fcst = ds_fcst[var_name]

# Alinear en el tiempo
#fcst, obs = xr.align(fcst, obs, join="inner")

# Calcular métricas
rmse_val = rmse(obs, fcst)
bias_val = bias(obs, fcst)
corr_val = pearson_correlation(obs, fcst)
d_index  = index_of_agreement(obs, fcst)
nse_val  = nse(obs, fcst)
kge_val  = kge(obs, fcst)
acc_1sigma = accuracy_within_sigma(obs, fcst, k=1.0)
#acc_2sigma = accuracy_within_sigma(obs, fcst, k=2.0) # agregar metricas aqui

# Crear dataset con resultados
ds_out = xr.Dataset(
    {
        "RMSE": rmse_val,
        "BIAS": bias_val,
        "Pearson_r": corr_val,
        "IoA": d_index,
        #"NSE": nse_val,
        "KGE": kge_val,
        "Accuracy_sigma": acc_1sigma,
        #"Accuracy_within_2sigma": acc_2sigma, # agregar metricas aqui
    }
)

# Guardar archivo
ds_out.to_netcdf(output_file)
print(f"Guardado: {output_file}")

