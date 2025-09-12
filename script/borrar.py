import xarray as xr
gribfile='/scratch/Datatemporal/SMN/data/regional/PERU_ETA22/2025/202501/2025010106/latlon_018'
gribfile='/scratch/Datatemporal/SMN/data/regional/PERU_WRF22/202501/2025010106/WRFPRS_d01.06'
ds = xr.open_dataset(
    gribfile,
    engine="cfgrib",
    backend_kwargs={
        'filter_by_keys': {
            #'typeOfLevel': 'heightAboveGround',
            "typeOfLevel": "surface",
            #'stepType': 'accum',
            #"stepType": "avg",
            #'typeOfLevel':'meanSea',
            #'shortName':'msl',
            #'level': 10,
            'stepType': 'instant',
            },
        'indexpath': ''},
    decode_times=False
)
print(ds)

