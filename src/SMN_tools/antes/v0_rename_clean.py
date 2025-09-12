import xarray as xr

def rename_and_clean(ds, new_dims):
    """
    Renombra dimensiones y limpia coordenadas innecesarias de un Dataset.
    
    Parámetros
    ----------
    ds : xr.Dataset
        Dataset abierto con xarray.
    new_dims : list
        Lista con los nuevos nombres de dimensiones.
        Ejemplo: ["new_time", "new_lat", "new_lon"] o ["time", "lat", "lon", "plev"]

    Retorna
    -------
    xr.Dataset
        Dataset con dimensiones renombradas y coords extra eliminadas.
    """
    rename_dims = {}
    for dim in ds.dims:
        if dim.lower() in ["latitude", "lat", "Lat", "Latitude", "Latitud", "latitud"]:
            rename_dims[dim] = new_dims[1]
        elif dim.lower() in ["longitude", "lon", "Lon", "Longitude", "Longitud", "longitud"]:
            rename_dims[dim] = new_dims[2]
        elif dim.lower() in ["t", "time", "Time"]:
            rename_dims[dim] = new_dims[0]
        elif dim.lower() in ["level", "levels", "lev", "plev", "isobaric", 
                             "isobaricinpa", "pressure", "pressurelevel"]:
            if len(new_dims) > 3:
                rename_dims[dim] = new_dims[3]
            else:
                rename_dims[dim] = "level"

    # Renombrar
    ds = ds.rename(rename_dims)

    # Dropear coords que no sean dims ni las nuevas coords
    keep_coords = list(rename_dims.values())
    drop_coords = [c for c in ds.coords if c not in keep_coords and c not in ds.dims]
    ds = ds.drop_vars(drop_coords, errors="ignore")

    return ds

