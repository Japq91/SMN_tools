#!/usr/bin/env python
# coding: utf-8

import os
import xarray as xr
import pandas as pd

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

r_in='/scratch/CMIP6_INTEP_LINEAL5km/geoestad/pisco' # <--- cambiar rutas de observado
r_out='%s/observado'%PARENT_DIR

### CREA OBSERVADO PISCO
ftmax='%s/tmax_daily_1981_2020_010.nc'%r_in
ftmin='%s/tmin_daily_1981_2020_010.nc'%r_in
dtn=xr.open_dataset(ftmin)['tmin']
print(dtn)
dtx=xr.open_dataset(ftmax)['tmax']
print(dtx)
ds = (dtn+dtx)/2
ds1=ds.to_dataset(name='t2m')
ds2=ds1.sel(time=slice('1981','2010'))
ds3=ds2.groupby('time.dayofyear').mean(dim='time')
ds3=ds3.rename({'dayofyear': 'time'})
ds3['time']=pd.date_range('2000-01-01', '2000-12-31', freq='D')
#
encoding = {var: {"zlib": True, "complevel": 5} for var in ds3.data_vars}
ds3.to_netcdf('%s/clima_pisco_t2m.nc'%r_out,encoding=encoding,format='NETCDF4')

### CREA OBSERVADO ERA5

