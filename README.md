# SMN_tools

**SMN_tools** es un paquete en Python diseñado para la **extracción, procesamiento, estandarización y fusión de salidas de modelos meteorológicos** (ETA y WRF), utilizadas en SENAMHI.  

El paquete transforma archivos **GRIB** en **NetCDF CF-1.8**, reorganizando variables y dimensiones para producir archivos listos para análisis y post-procesamiento.

---

##  Dependencias y versiones

Este paquete requiere **Python >= 3.9**.  
Las librerías y versiones exactas están definidas en [`pyproject.toml`](pyproject.toml):

- `xarray==2025.9.0`  
- `cfgrib==0.9.15.0`  
- `numpy==2.3.3`  
- `netCDF4==1.7.2`  
- `h5netcdf==1.6.4`  

Dependencias adicionales incluidas en `requirements.txt`:
- `pandas==2.3.2`  
- `eccodes==2.43.0`  
- `h5py==3.14.0`  

---

##  Estructura del proyecto

```

SMN\_tools/
├── pyproject.toml        # Configuración PEP 621 (paquete y dependencias)
├── requirements.txt      # Dependencias congeladas
├── setup.py              # Instalación alternativa
├── script/
│   └── test\_extrac.py    # Ejemplo completo de flujo de trabajo
├── src/
│   └── SMN\_tools/        # Código fuente
│       ├── ETA\_extrae.py     # Extracción ETA
│       ├── WRF\_extrae.py     # Extracción WRF
│       ├── procesa\_netcdf.py # Procesamiento de NetCDF
│       ├── merge\_netcdf.py   # Fusión de variables
│       ├── rename\_clean.py   # Estandarización de variables/dimensiones
│       ├── delete\_files.py   # Limpieza de directorios
│       ├── **init**.py       # API pública del paquete
│       └── **main**.py       # Punto de entrada
└── SMN\_tools.egg-info/   # Metadatos de instalación

```

---

##  Instalación

Clonar el repositorio e instalar en modo editable:

```bash
git clone https://github.com/usuario/SMN_tools.git
cd SMN_tools
pip install -e .
```

---

##  Detalle de scripts principales

### 1. **ETA\_extrae.py**

* Función: `extrac_ETA(out_path, gribfile, tipo)`
* Extrae variables atmosféricas de archivos **GRIB ETA**:

  * Precipitación (`tp`)
  * Viento en niveles isobáricos (`level_vars`: u, v en 925, 850, 500, 200 hPa)
  * Presión reducida al nivel del mar (`mslp`)
  * Viento a 10 m (`wind10m`: u10, v10)
  * Temperatura a 2 m (`t2m`)
  * Humedad relativa a 2 m (`r2m`)
  * Radiación de onda corta descendente (`ssrd`)
* Genera archivos NetCDF individuales por variable y paso temporal.

---

### 2. **WRF\_extrae.py**

* Función: `extrac_WRF(out_path, gribfile, tipo)`
* Procesa salidas **WRF GRIB** y extrae variables:

  * Precipitación acumulada (`tp`)
  * Vientos, temperatura, humedad relativa y geopotencial en niveles (`level_vars`)
  * Presión al nivel del mar (`mslp`)
  * Viento a 10 m (`10u`, `10v`)
  * Temperatura a 2 m (`t2m`)
  * Temperatura de rocío a 2 m (`d2m`)
  * Humedad relativa a 2 m (`r2m`)
* Incluye función auxiliar `make_structured()` para reorganizar datasets en grillas regulares (lat/lon, opcional z).

---

### 3. **procesa\_netcdf.py**

* Función: `process_netcdf_files(list_files, prefix_out, new_dims)`
* **Objetivo**:

  * Uniformiza NetCDFs generados en la fase de extracción.
  * Renombra variables y dimensiones.
  * Concatena archivos a lo largo del tiempo.
  * Añade metadatos estándar CF.
* Dimensiones soportadas:

  * Superficie: `["time","lat","lon"]`
  * Niveles: `["time","lev","lat","lon"]`.

---

### 4. **merge\_netcdf.py**

* Función: `merge_files(list_files, output_file, institution="SENAMHI", source=None)`
* Une múltiples archivos NetCDF procesados en un solo producto.
* Añade metadatos globales compatibles con CF-1.8 (`institution`, `source`, `history`, `references`).
* Comprime variables con `zlib`.

---

### 5. **rename\_clean.py**

* Función: `rename_and_clean(input_file, output_file, var_name_out, dims_out)`
* Renombra dimensiones y variables para uniformizar productos NetCDF.
* Elimina coordenadas innecesarias (`valid_time`, `forecast_reference_time`).
* Configura compresión (`zlib`).
* Retorna un dataset limpio listo para concatenación o fusión.

---

### 6. **delete\_files.py**

* Función: `clean_outdir(outdir)`
* Elimina todos los archivos `.nc` de un directorio de salida.
* Útil para limpiar corridas anteriores antes de procesar nuevas.

---

### 7. ****init**.py**

Expone las funciones principales del paquete:

```python
from .ETA_extrae import extrac_ETA
from .WRF_extrae import extrac_WRF
from .procesa_netcdf import process_netcdf_files
from .rename_clean import rename_and_clean
from .merge_netcdf import merge_files
from .delete_files import clean_outdir
```

---

##  Flujo de trabajo

1. **Definir modelo, fecha y carpeta de salida**
2. **Extraer variables ETA/WRF en NetCDF individuales**
3. **Procesar y concatenar archivos por variable**
4. **Unir variables de superficie o niveles en un archivo final**

Ejemplo resumido:

```python
from SMN_tools import extrac_WRF, process_netcdf_files, merge_files, clean_outdir

# 1. Limpieza
clean_outdir("out/")

# 2. Extracción desde GRIB
extrac_WRF("out/", "WRFPRS_d01.00", tipo=["wind10m","t2m","mslp"])

# 3. Procesamiento (unificar tiempos y renombrar dims)
process_netcdf_files(["out/10u_000.nc","out/10v_000.nc"], prefix_out="sfc", new_dims=["time","lat","lon"])

# 4. Fusión en archivo final
merge_files(["out/sfc_tmp_10u.nc","out/sfc_tmp_10v.nc"], "out/WRF_20250101_sfc.nc")
```

Salida final: `WRF_20250101_sfc.nc` y/o `WRF_20250101_prs.nc` listos para análisis.

---

## Licencia

MIT License.

