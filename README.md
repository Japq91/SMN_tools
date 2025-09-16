# SMN_tools

**SMN_tools** es un paquete en Python diseñado para la **extracción, procesamiento, estandarización y fusión de salidas de modelos meteorológicos** (ETA y WRF), utilizadas en SENAMHI.  

El paquete transforma archivos **GRIB** en **NetCDF CF-1.8**, reorganizando variables y dimensiones para producir archivos listos para análisis y post-procesamiento.

---

##  Dependencias y versiones

Este paquete requiere **Python >= 3.9**.  
Las librerías principales y sus versiones mínimas están definidas en [`pyproject.toml`](pyproject.toml):

- `xarray>=2023.12.0`  
- `cfgrib>=0.9.14.0`  
- `numpy>=1.26.4`  
- `netCDF4>=1.6.5`  
- `h5netcdf>=1.2.0`  
- `ipykernel>=6.0.0`  

Dependencias adicionales incluidas en `requirements.txt`:
- `pandas`  
- `eccodes`  
- `h5py`  
- `matplotlib>=3.7.0` (visualización de datos y mapas)
- `pillow>=9.0.0` (soporte de imágenes para matplotlib)

---

##  Instalación

Clonar el repositorio y ejecutar el instalador con **Makefile**:

```bash
git clone https://github.com/Japq91/SMN_tools.git
cd SMN_tools
make install
```

Este comando realiza dos pasos automáticamente:

1. Instala el paquete en modo editable (`pip install -e .`).
2. Registra el kernel de Jupyter llamado **Python (smn\_tools)**.

---

## Uso en Jupyter Lab

Al abrir **Jupyter Lab**, selecciona el kernel:

```
Kernel → Change Kernel → Python (smn_tools)
```

De esta forma, tus notebooks podrán usar las librerías del entorno virtual donde instalaste **SMN\_tools**.

---

## Estructura del proyecto

```
SMN_tools/
├── pyproject.toml        # Configuración PEP 621 (paquete y dependencias)
├── requirements.txt      # Dependencias congeladas
├── Makefile              # Instalación rápida con make install
├── script/
│   └── test_extrac.py    # Ejemplo completo de flujo de trabajo
├── src/
│   └── SMN_tools/        # Código fuente
│       ├── ETA_extrae.py
│       ├── WRF_extrae.py
│       ├── procesa_netcdf.py
│       ├── merge_netcdf.py
│       ├── rename_clean.py
│       ├── delete_files.py
│       ├── scripts/
│       │   └── install_kernel.py  # kernel en Jupyter
│       ├── __init__.py
│       └── __main__.py
└── SMN_tools.egg-info/
```
---

##  Detalle de scripts principales

### 1. Extracción de variables: `ETA_extrae.py` y `WRF_extrae.py`

Los scripts **`ETA_extrae.py`** y **`WRF_extrae.py`** contienen las funciones principales para la **extracción de variables meteorológicas desde archivos GRIB** generados por los modelos **ETA** y **WRF**.  
Ambos convierten las variables en **archivos NetCDF individuales por variable y paso temporal**, facilitando el procesamiento y análisis posterior.

- **Función ETA**: `extrac_ETA(out_path, gribfile, tipo)`  
- **Función WRF**: `extrac_WRF(out_path, gribfile, tipo)`  

#### Variables soportadas

- **Comunes a ambos modelos**
  - Precipitación acumulada (`tp`)
  - Viento en niveles isobáricos (`level_vars`: u, v en 925, 850, 500, 200 hPa)
  - Presión al nivel del mar (`mslp`)
  - Viento a 10 m (`wind10m`: u10, v10 / `10u`, `10v`)
  - Temperatura a 2 m (`t2m`)
  - Humedad relativa a 2 m (`r2m`)

- **Específicas de ETA**
  - Radiación de onda corta descendente (`ssrd`)

- **Específicas de WRF**
  - Temperatura de rocío a 2 m (`d2m`)
  - Geopotencial en niveles (`gh`)

#### Funciones adicionales

- `WRF_extrae.py` incluye la función auxiliar **`make_structured()`**, que reorganiza los datasets en grillas regulares con coordenadas únicas de latitud y longitud, y opcionalmente un eje vertical (`z`), asegurando compatibilidad para análisis posteriores.


### 2. **procesa\_netcdf.py**

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

### 3. **rename\_clean.py**

* Función: `rename_and_clean(input_file, output_file, var_name_out, dims_out)`
* Renombra dimensiones y variables para uniformizar productos NetCDF.
* Elimina coordenadas innecesarias (`valid_time`, `forecast_reference_time`).
* Configura compresión (`zlib`).
* Retorna un dataset limpio listo para concatenación o fusión.
---

### 4. **merge\_netcdf.py**

* Función: `merge_files(list_files, output_file, institution="SENAMHI", source=None)`
* Une múltiples archivos NetCDF procesados en un solo producto.
* Añade metadatos globales compatibles con CF-1.8 (`institution`, `source`, `history`, `references`).
* Comprime variables con `zlib`.
---

### 5. **delete\_files.py**

* Función: `clean_outdir(outdir)`
* Elimina todos los archivos `.nc` de un directorio de salida.
* Útil para limpiar corridas anteriores antes de procesar nuevas.
---

### 6. **\_\_init\_\_.py**

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

El flujo de trabajo completo está ejemplificado en [`script/test_extrac.py`](script/test_extrac.py).  
Consta de **cuatro etapas principales**, que van desde la preparación de la corrida hasta la generación de archivos NetCDF finales de superficie (`sfc`) y niveles (`prs`).

1. **Definir modelo, fecha y carpeta de salida**
2. **Extraer variables ETA/WRF en NetCDF individuales**
3. **Procesar y concatenar archivos por variable**
4. **Unir variables de superficie o niveles en un archivo final**

Ejemplo resumido:

---

#### 1. Definir modelo, fecha y carpeta de salida
Se configura el modelo a usar (`PERU_ETA22` o `PERU_WRF22`), así como fecha y hora de la corrida.  
Además, se prepara la carpeta de salida y se limpian archivos `.nc` de corridas anteriores:

```python
model = "PERU_ETA22"   # o "PERU_WRF22"
hor, dia, mes, yea = "06", "01", "01", "2025"

outdir = f"/ruta/out/{model}"
os.system(f'mkdir -p {outdir}')
clean_outdir(outdir)   # elimina archivos previos
```

---

#### 2. Extraer variables ETA/WRF en NetCDF individuales

Dependiendo del modelo, se seleccionan archivos GRIB y se extraen las variables solicitadas.
Ejemplo para ETA:

```python
tipos = ['tp','level_vars','wind10m','t2m','r2m','ssrd','mslp']

for file_p in files_prono:
    if "ETA" in model: extrac_ETA(outdir, file_p, tipos)
    if "WRF" in model: extrac_WRF(outdir, file_p, tipos)
```

Cada variable se guarda como un archivo NetCDF independiente en la carpeta de salida, con su respectivo timestamp.

---

#### 3. Procesar y concatenar archivos por variable

Una vez extraídas, las variables deben estandarizarse en dimensiones y concatenarse en el tiempo.

* Para **superficie** (`sfc`): se usan dimensiones `["time","lat","lon"]`.
* Para **niveles de presión** (`prs`): se usan dimensiones `["time","lev","lat","lon"]`.

```python
for var_in in ['prs','sfc']:
    if var_in == 'prs':
        nueva_lista = ['u','v']   # variables en niveles
        new_dims0 = ["time","lev","lat","lon"]
    else:
        nueva_lista = ['tp','10u','10v','t2m','r2m','mslp','ssrd']
        new_dims0 = ["time","lat","lon"]

    for var in nueva_lista:
        files_vars = gb(f'{outdir}/{var}_*')
        process_netcdf_files(files_vars, prefix_out=var_in, new_dims=new_dims0)
```

Esto produce archivos intermedios con prefijo `sfc_tmp_` o `prs_tmp_`.

---

#### 4. Unir variables de superficie o niveles en un archivo final

Finalmente, todas las variables de superficie (`sfc`) o niveles (`prs`) se combinan en un único NetCDF comprimido con metadatos CF-1.8:

```python
for var_in in ['prs','sfc']:
    files_variables = gb(f"{outdir}/{var_in}_*")
    if len(files_variables) == 0: continue

    final_name = f"{model}_{yea}{mes}{dia}{hor}_{var_in}.nc"
    out_file = os.path.join(run_dir, final_name)

    merge_files(files_variables, out_file)
```

---

#### Salida final

* `PERU_ETA22_2025010106_sfc.nc`
* `PERU_ETA22_2025010106_prs.nc`

o, en el caso de WRF:

* `PERU_WRF22_2025010106_sfc.nc`
* `PERU_WRF22_2025010106_prs.nc`
---

## Licencia

MIT License.

