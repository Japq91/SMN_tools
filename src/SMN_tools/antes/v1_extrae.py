import xarray as xr
import numpy as np

def reorganizar_dataset(dataset, var_name, coord_lat='latitude', coord_lon='longitude', coord_z=None):
    """Reorganiza un dataset para que las coordenadas de lat/lon sean únicas."""
    latitudes_unicas = np.unique(dataset[coord_lat].values)
    longitudes_unicas = np.unique(dataset[coord_lon].values)

    time_data = dataset['time'].values if 'time' in dataset.coords else None
    valid_time_data = dataset['valid_time'].values if 'valid_time' in dataset.coords else None

    if coord_z and coord_z in dataset.coords:
        var_reshaped = dataset[var_name].values.reshape(
            (dataset[var_name].shape[0], len(latitudes_unicas), len(longitudes_unicas))
        )
        nuevo_dataset = xr.Dataset(
            {var_name: ([coord_z, coord_lat, coord_lon], var_reshaped)},
            coords={coord_z: dataset.coords[coord_z],
                    coord_lat: latitudes_unicas,
                    coord_lon: longitudes_unicas}
        )
    else:
        var_reshaped = dataset[var_name].values.reshape(
            (len(latitudes_unicas), len(longitudes_unicas))
        )
        nuevo_dataset = xr.Dataset(
            {var_name: ([coord_lat, coord_lon], var_reshaped)},
            coords={coord_lat: latitudes_unicas,
                    coord_lon: longitudes_unicas}
        )

    if time_data is not None:
        nuevo_dataset = nuevo_dataset.assign_coords(time=time_data)
    if valid_time_data is not None:
        nuevo_dataset = nuevo_dataset.assign_coords(valid_time=valid_time_data)

    return nuevo_dataset


def extrac_ETA(gribfile):
    """Extrae variables meteorológicas del modelo ETA en formato GRIB."""

    # Isobáricas
    uprs = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': 'u'},
            'indexpath': ''
        },
        decode_timedelta=False
    )
    vprs = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': 'v'},
            'indexpath': ''
        },
        decode_timedelta=False
    )
    tprs = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': 't'},
            'indexpath': ''
        },
        decode_timedelta=False
    )

    # Superficie
    landsfc = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'surface', 'shortName': 'lsm'},
            'indexpath': ''
        },
        decode_timedelta=False
    )
    pressfc = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'surface', 'shortName': 'sp'},
            'indexpath': ''
        },
        decode_timedelta=False
    )

    # Presión al nivel del mar
    prmsl = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'typeOfLevel': 'meanSea', 'shortName': 'mslet'},
            'indexpath': ''
        },
        decode_timedelta=False
    )

    # Viento 10m
    v10m = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'paramId': 166},
            'indexpath': ''
        },
        decode_timedelta=False
    )
    u10m = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'paramId': 165},
            'indexpath': ''
        },
        decode_timedelta=False
    )

    # 2m
    d2m = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'paramId': 168},
            'indexpath': ''
        },
        decode_timedelta=False
    )
    t2m = xr.open_dataset(
        gribfile, engine='cfgrib',
        backend_kwargs={
            'filter_by_keys': {'paramId': 167},
            'indexpath': ''
        },
        decode_timedelta=False
    )

    # Reorganizar
    uprs = reorganizar_dataset(uprs, 'u', coord_z='isobaricInhPa')
    vprs = reorganizar_dataset(vprs, 'v', coord_z='isobaricInhPa')
    tprs = reorganizar_dataset(tprs, 't', coord_z='isobaricInhPa')
    landsfc = reorganizar_dataset(landsfc, 'lsm')
    pressfc = reorganizar_dataset(pressfc, 'sp')
    prmsl = reorganizar_dataset(prmsl, 'mslet')
    v10m = reorganizar_dataset(v10m, 'v10')
    u10m = reorganizar_dataset(u10m, 'u10')
    d2m = reorganizar_dataset(d2m, 'd2m')
    t2m = reorganizar_dataset(t2m, 't2m')

    return {
        'uprs': uprs,
        'vprs': vprs,
        'tprs': tprs,
        'landsfc': landsfc,
        'pressfc': pressfc,
        'prmsl': prmsl,
        'u10m': u10m,
        'v10m': v10m,
        't2m': t2m,
        'd2m': d2m
    }

