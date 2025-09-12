import xarray as xr
import numpy as np

def normalizar_a_superficie(ds, var_name):
    """
    Normaliza variables de superficie para que todas tengan una dimensión estándar 'superficie'.
    Quita coordenadas verticales (ej. level, heightAboveGround) y añade superficie='surface'.
    """
    arr = ds[var_name]

    # Quitar coordenadas verticales si existen
    for coord in ['heightAboveGround', 'surface']:
        if coord in arr.coords:
            arr = arr.drop_vars(coord)

    # Expandir con dimensión común 'superficie'
    arr = arr.expand_dims({'superficie': ['surface']})

    return xr.Dataset({var_name: arr})


def extrac_ETA(gribfile):
    """
    Extrae variables meteorológicas del modelo ETA en formato GRIB.

    Incluye:
    - Presión al nivel del mar (mslet)
    - Temperatura y humedad relativa a 2m (2t, 2r)
    - Viento 10m (u10, v10)
    - Precipitación total (tp)
    - Radiación onda corta descendente (msdwswrf)
    - Viento en niveles isobáricos (u, v)
    """

    # --- Viento en niveles isobáricos ---
    uprs = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': 'u'}, 'indexpath': ''},
        decode_timedelta=False
    )
    vprs = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': 'v'}, 'indexpath': ''},
        decode_timedelta=False
    )

    # --- Presión al nivel del mar ---
    prmsl = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'meanSea', 'shortName': 'mslet'}, 'indexpath': ''},
        decode_timedelta=False
    )
    prmsl = normalizar_a_superficie(prmsl, 'mslet')

    # --- Viento 10m ---
    u10m = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10, 'shortName': 'u10'}, 'indexpath': ''},
        decode_timedelta=False
    )
    v10m = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10, 'shortName': 'v10'}, 'indexpath': ''},
        decode_timedelta=False
    )
    u10m = normalizar_a_superficie(u10m, 'u10')
    v10m = normalizar_a_superficie(v10m, 'v10')

    # --- Temperatura y humedad 2m ---
    t2m = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2, 'shortName': '2t'}, 'indexpath': ''},
        decode_timedelta=False
    )
    r2m = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2, 'shortName': '2r'}, 'indexpath': ''},
        decode_timedelta=False
    )
    t2m = normalizar_a_superficie(t2m, '2t')
    r2m = normalizar_a_superficie(r2m, '2r')

    # --- Precipitación total ---
    tp = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface', 'shortName': 'tp'}, 'indexpath': ''},
        decode_timedelta=False
    )
    tp = normalizar_a_superficie(tp, 'tp')

    # --- Radiación onda corta descendente ---
    ssrd = xr.open_dataset(
        gribfile, engine="cfgrib",
        backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface', 'shortName': 'msdwswrf'}, 'indexpath': ''},
        decode_timedelta=False
    )
    ssrd = normalizar_a_superficie(ssrd, 'msdwswrf')

    return {
        'uprs': uprs,
        'vprs': vprs,
        'prmsl': prmsl,
        'u10m': u10m,
        'v10m': v10m,
        't2m': t2m,
        'r2m': r2m,
        'tp': tp,
        'ssrd': ssrd,
    }

