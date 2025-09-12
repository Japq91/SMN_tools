import os
import xarray as xr

def process_netcdf_files(list_files, prefix_out, new_dims=["time", "lat", "lon"]):
    """
    Une varios archivos NetCDF en la dimensión 'time',
    renombra dimensiones y variables, elimina coordenadas no deseadas,
    y guarda en un archivo comprimido.

    Parámetros:
    -----------
    list_files : list
        Lista de rutas de archivos NetCDF, ej: ["10u_006.nc", "10u_009.nc", ...]
    prefix_out : str
        Prefijo para el nombre final, ej: "sfc"
    new_dims : list
        Lista con los nuevos nombres de dimensiones, ej: ["new_time", "new_lat", "new_lon"]
        El orden debe ser [time, lat, lon].
    """
    if len(new_dims) != 3:
        raise ValueError("new_dims debe contener exactamente tres nombres: [time, lat, lon].")

    datasets = []
    for file in list_files:
        # Obtener el nombre de la variable desde el archivo
        var_name = os.path.basename(file).split("_")[0]
        
        # Abrir el archivo
        ds = xr.open_dataset(file)

        # Renombrar dimensiones a los nuevos nombres
        rename_dims = {}
        for dim in ds.dims:
            if dim.lower() in ["latitude", "lat","Lat","Latitude","Latitud","latitud"]:
                rename_dims[dim] = new_dims[1]
            elif dim.lower() in ["longitude", "lon","Lon","Longitude","Longitud","longitud"]:
                rename_dims[dim] = new_dims[2]
            elif dim.lower() in ["t", "time","Time"]:
                rename_dims[dim] = new_dims[0]
        ds = ds.rename(rename_dims)

        # Dropear coordenadas/dimensiones que no están en los nuevos nombres
        drop_coords = [c for c in ds.coords if c not in new_dims]
        ds = ds.drop_vars(drop_coords, errors="ignore")

        # Renombrar la variable al nombre extraído
        if len(ds.data_vars) == 1:
            old_var = list(ds.data_vars)[0]
            ds = ds.rename({old_var: var_name})
        else:
            raise ValueError(f"El archivo {file} tiene más de una variable, se esperaba solo una.")

        datasets.append(ds)

    # Concatenar en la dimensión de tiempo (usando el nuevo nombre)
    combined = xr.concat(datasets, dim=new_dims[0])
    
    # Definir nombre de salida
    out_dir = os.path.dirname(list_files[0])
    out_file = os.path.join(out_dir, f"tmp_{prefix_out}_{var_name}.nc")
    
    # Guardar con compresión
    encoding = {var: {"zlib": True, "complevel": 5} for var in combined.data_vars}
    combined.to_netcdf(out_file, encoding=encoding)
    
    print(f"Archivo generado: {out_file}")

# ================================
# Ejemplo de uso:
# files = ["10u_006.nc", "10u_009.nc", "10u_012.nc"]
# process_netcdf_files(files, prefix_out="sfc", new_dims=["new_time", "new_lat", "new_lon"])

