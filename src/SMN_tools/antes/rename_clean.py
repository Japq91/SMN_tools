import xarray as xr

def rename_and_clean(ds: xr.Dataset, new_dims: list) -> xr.Dataset:
    """
    Limpia coords basura, setea coords horizontales si es ungrid,
    renombra dims y añade atributos CF.
    """

    # 1. Dropear coords basura
    drop_candidates = ["step", "valid_time", "heightAboveGround"]
    ds = ds.drop_vars([c for c in drop_candidates if c in ds.coords], errors="ignore")

    # 2. Si el grid es unstructured (ej. dimensión "points")
    # asegurar que lat/lon queden como coordenadas asociadas a esa dimensión
    if "latitude" in ds and "longitude" in ds:
        for dim in ds.dims:
            if ds["latitude"].sizes.get(dim) == ds.sizes[dim]:
                ds = ds.assign_coords({
                    "latitude": (dim, ds["latitude"].values),
                    "longitude": (dim, ds["longitude"].values)
                })

    # 3. Renombrar dimensiones
    lat_names = ["latitude", "lat", "latitud"]
    lon_names = ["longitude", "lon", "longitud"]
    time_names = ["time", "t"]
    lev_names = ["level", "levels", "lev", "plev",
                 "isobaric", "isobaricinpa", "pressure", "pressurelevel"]

    rename_dims = {}
    for dim in ds.dims:
        d = dim.lower()
        if d in lat_names:
            rename_dims[dim] = new_dims[1]
        elif d in lon_names:
            rename_dims[dim] = new_dims[2]
        elif d in time_names:
            rename_dims[dim] = new_dims[0]
        elif len(new_dims) == 4 and d in lev_names:
            rename_dims[dim] = new_dims[3]

    ds = ds.rename(rename_dims)

    # 4. Añadir atributos CF
    if new_dims[0] in ds.coords:
        ds[new_dims[0]].attrs.update({"standard_name": "time", "long_name": "Time", "axis": "T"})
    if new_dims[1] in ds.coords:
        ds[new_dims[1]].attrs.update({"standard_name": "latitude", "long_name": "Latitude",
                                      "units": "degrees_north", "axis": "Y"})
    if new_dims[2] in ds.coords:
        ds[new_dims[2]].attrs.update({"standard_name": "longitude", "long_name": "Longitude",
                                      "units": "degrees_east", "axis": "X"})
    if len(new_dims) == 4 and new_dims[3] in ds.coords:
        ds[new_dims[3]].attrs.update({"standard_name": "air_pressure", "long_name": "Pressure level",
                                      "units": "hPa", "positive": "down", "axis": "Z"})

    return ds

