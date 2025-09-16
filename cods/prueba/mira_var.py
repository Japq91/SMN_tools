import xarray as xr
#ETA
#gribfile="/scratch/Datatemporal/SMN/data/regional/PERU_ETA22/2025/202501/2025010106/latlon_000"
# WRF
gribfile="/scratch/Datatemporal/SMN/data/regional/PERU_WRF22/202501/2025010106/WRFPRS_d01.00"
#
ds = xr.open_dataset(gribfile, engine="cfgrib",
            backend_kwargs={'filter_by_keys': {'shortName': 'tp',}, 'indexpath': ''},
            decode_timedelta=False)
print(ds)

