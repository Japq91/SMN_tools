import xarray as xr
files='/scratch/SMN_tools/out/PERU_ETA22/10v_012.nc'
ds=xr.open_dataset(files)
print(ds)
