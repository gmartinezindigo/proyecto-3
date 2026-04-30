# Datos Google Earth Engine — Pesos, Bandas y Decisión de Formato

> Consultas ejecutadas en GEE con `project='charming-mile-436804-q2'` el 2026-04-29.  
> Resultados completos en [`docs/gee_query_results.json`](gee_query_results.json).  
> AOI: `[-76.60, 3.30, -76.40, 3.55]` → **619.6 km²** (22.3 km × 27.8 km)  
> Período base: **2018-01-01 → 2026-04-29**

---

## 1. Conteo Real de Imágenes (GEE)

| Dataset | Collection ID | Inicio real | N° imágenes en AOI | Resolución | Bandas totales |
|---|---|---|---|---|---|
| S5P NO₂ | `COPERNICUS/S5P/OFFL/L3_NO2` | 2018-06-28 | **40,064** | 1113.2 m | 12 |
| S5P SO₂ | `COPERNICUS/S5P/OFFL/L3_SO2` | 2018-12-05 | **38,176** | 1113.2 m | 10 |
| S5P O₃ | `COPERNICUS/S5P/OFFL/L3_O3` | 2018-09-08 | **38,876** | 1113.2 m | 7 |
| Sentinel-2 SR | `COPERNICUS/S2_SR_HARMONIZED` | 2018-01-01 | **1,136** | 10/20/60 m | 24 |
| ERA5-Land | `ECMWF/ERA5_LAND/HOURLY` | 2018-01-01 | **72,850** | 11132 m | 8+ |
| ERA5 (BLH) | `ECMWF/ERA5/HOURLY` | 2018-01-01 | *(pendiente)* | 27830 m | 1 |
| MODIS AOD | `MODIS/061/MCD19A2_GRANULES` | 2018-01-01 | **245,155** | 1000 m | 13 |
| **TOTAL** | | | **436,267** | | |

**Notas sobre conteos:**
- **S5P (~14 imgs/día):** Swath de 2600 km cubre todas las longitudes en la franja ecuatorial por órbita. GEE almacena cada órbita como imagen independiente (L3 por órbita).
- **ERA5 (72,850 imgs):** 8 años × 365 días × 24 horas = 70,080 horas esperadas. Consistente.
- **MODIS (245,155 imgs):** `MCD19A2_GRANULES` son segmentos de 5 minutos de órbita (Terra + Aqua). `filterBounds` retorna toda granula cuya huella cruza el AOI → ~84/día. Para análisis temporal se promedian por día.
- **Sentinel-2 (1,136 imgs):** S2A + S2B combinados dan revisita ~2.5 días efectivos. 8 años × 365/2.5 ≈ 1,168 esperados. Consistente.

---

## 2. Bandas Seleccionadas por Dataset

### 2.1 Sentinel-5P NO₂ — 2 de 12 bandas

| Banda | Unidades | ¿Usar? | Justificación |
|---|---|---|---|
| `tropospheric_NO2_column_number_density` | mol/m² | **SÍ** | Variable primaria (situacion1.md: *"columnas troposféricas de NO₂"*). Excluye componente estratosférica irrelevante para calidad del aire superficial. |
| `cloud_fraction` | fracción | **SÍ** | Filtrado QA: imágenes con cloud_fraction > 0.3 degradan el retrieval de NO₂. |
| `NO2_column_number_density` | mol/m² | No | Columna total (troposférica + estratosférica). La troposférica es suficiente. |
| `stratospheric_NO2_column_number_density` | mol/m² | No | Componente estratosférica. No relevante para calidad del aire urbano. |
| `NO2_slant_column_number_density` | mol/m² | No | Columna slant sin corrección AMF. Se usa la vertical corregida. |
| `tropopause_pressure` | Pa | No | Variable auxiliar de retrieval. |
| `absorbing_aerosol_index` | adim. | No | Cubierto por MODIS MCD19A2 con mayor resolución espacial. |
| `sensor_altitude/azimuth/zenith`, `solar_azimuth/zenith` | — | No | Metadatos orbitales. No entran al panel analítico. |

### 2.2 Sentinel-5P SO₂ — 2 de 10 bandas

| Banda | Unidades | ¿Usar? | Justificación |
|---|---|---|---|
| `SO2_column_number_density` | mol/m² | **SÍ** | Variable primaria (situacion1.md: *"SO₂ vertical column"*). Columna vertical a nivel del suelo. |
| `cloud_fraction` | fracción | **SÍ** | QA: `cloud_fraction_crb < 0.3` requerido según documentación GEE del producto. |
| `SO2_column_number_density_15km` | mol/m² | No | Columna a 15 km para erupciones volcánicas. El AOI no tiene volcanes activos. |
| `SO2_column_number_density_amf` | mol/m² | No | Factor AMF: variable de retrieval, no de análisis ambiental. |
| `SO2_slant_column_number_density` | mol/m² | No | Columna slant sin corrección geométrica. |
| `absorbing_aerosol_index` | adim. | No | Duplicado de la banda en NO₂ y cubierto por MODIS. |
| Ángulos orbitales/solares | — | No | Metadatos orbitales. |

### 2.3 Sentinel-5P O₃ — 2 de 7 bandas

| Banda | Unidades | ¿Usar? | Justificación |
|---|---|---|---|
| `O3_column_number_density` | mol/m² | **SÍ** | Variable primaria (situacion1.md: *"O₃ total column"*). |
| `cloud_fraction` | fracción | **SÍ** | Filtrado QA del retrieval de O₃. |
| `O3_effective_temperature` | K | No | Temperatura efectiva de sección transversal: auxiliar de algoritmo, no de análisis. |
| Ángulos orbitales/solares | — | No | Metadatos orbitales. |

### 2.4 Sentinel-2 SR — 15 de 24 bandas

| Banda | Res. | Longitud de onda | ¿Usar? | Justificación |
|---|---|---|---|---|
| `B1` | 60 m | 443.9 nm | **SÍ** | Proxy de aerosoles finos. Complementa MODIS AOD a mayor resolución. |
| `B2` | 10 m | 496.6 nm | **SÍ** | Azul. Base para NDWI y corrección atmosférica. Corredor industrial Yumbo-Acopi. |
| `B3` | 10 m | 560 nm | **SÍ** | Verde. NDWI y RGB visual. Monitoreo de cultivos de caña (norte del Valle). |
| `B4` | 10 m | 664.5 nm | **SÍ** | Rojo. Componente del NDVI para biomasa en caña y coberturas industriales. |
| `B5` | 20 m | 703.9 nm | **SÍ** | Red Edge 1. Sensible al contenido de clorofila. Indicador de estrés por contaminación. |
| `B6` | 20 m | 740.2 nm | **SÍ** | Red Edge 2. Índices CIre, NDRE. Complementa B5. |
| `B7` | 20 m | 782.5 nm | **SÍ** | Red Edge 3. Mejora estimación de LAI en caña de azúcar. |
| `B8` | 10 m | 835.1 nm | **SÍ** | NIR principal. NDVI, EVI, análisis de cambio de cobertura. Alta prioridad. |
| `B8A` | 20 m | 864.8 nm | **SÍ** | NIR estrecho. Índices de vegetación de precisión, menos sensible a variación atmosférica. |
| `B9` | 60 m | 945 nm | **SÍ** | Vapor de agua. Covariable de corrección y cruce con ERA5 precipitable water. |
| `B11` | 20 m | 1613.7 nm | **SÍ** | SWIR 1. Humedad foliar y del suelo. Seguimiento de quemas de caña, suelo desnudo. |
| `B12` | 20 m | 2202.4 nm | **SÍ** | SWIR 2. Detección de áreas urbanas e industriales. Delimitación corredor Yumbo-Acopi. |
| `AOT` | 10 m | — | **SÍ** | AOD sen2cor a 10 m. Resolución superior a MODIS (1 km) para análisis intra-urbano. |
| `SCL` | 20 m | — | **SÍ** | Scene Classification Layer (valores 1-11). Imprescindible para enmascarar nubes, sombras, agua. |
| `QA60` | 60 m | — | **SÍ** | Bitmask de nubes (bit 10: nubes opacas, bit 11: cirrus). Complementa SCL en validación cruzada. |
| `WVP` | 10 m | — | No | Redundante con B9 y ERA5 dewpoint. Derivable en postproceso. |
| `TCI_R/G/B` | 10 m | — | No | Imágenes visuales derivadas de B4/B3/B2. Redundantes con bandas raw. |
| `MSK_CLDPRB` | 20 m | — | No | Probabilidad de nubes. SCL ya provee clasificación suficiente. |
| `MSK_SNWPRB` | 10 m | — | No | Probabilidad de nieve. Cali (3.4°N, ~1000 m snm) no tiene cobertura de nieve. |

### 2.5 ERA5-Land — 6 de 8+ bandas + colección adicional para BLH

| Banda | Unidades | ¿Usar? | Justificación |
|---|---|---|---|
| `temperature_2m` | K | **SÍ** | T2m explícita en situacion1.md. |
| `dewpoint_temperature_2m` | K | **SÍ** | Necesaria para derivar RH = f(T2m, Td) vía fórmula Magnus. RH requerida por situacion1.md. |
| `u_component_of_wind_10m` | m/s | **SÍ** | Componente zonal del viento. situacion1.md requiere "viento". |
| `v_component_of_wind_10m` | m/s | **SÍ** | Componente meridional. Junto con u → velocidad y dirección. |
| `surface_pressure` | Pa | **SÍ** | Necesaria para conversión mol/m² → µg/m³ al integrar con S5P. |
| `total_precipitation_hourly` | m | **SÍ** | Precipitación horaria (wet deposition). Afecta scavenging de NO₂, SO₂ y aerosoles. |
| `forecast_albedo` | adim. | No | Albedo superficial. No requerido directamente por el panel de situacion1.md. |

> **⚠️ ERROR EN ENUNCIADO — BLH:** `boundary_layer_height` aparece en situacion1.md bajo ERA5-Land. Verificado contra documentación oficial GEE (2026-04-29): **ERA5-Land no contiene BLH**. La única variable de capa límite en ERA5-Land es `lake_mix_layer_depth`, específica de cuerpos de agua. BLH pertenece a ERA5 atmosférico (`ECMWF/ERA5/HOURLY`), que es una colección diferente no listada en el proyecto. Se documenta como inconsistencia del enunciado y **no se agrega nueva colección**. Las variables seleccionadas para ERA5-Land son las confirmadas disponibles.

### 2.6 MODIS MCD19A2 — 4 de 13 bandas

| Banda | Unidades | ¿Usar? | Justificación |
|---|---|---|---|
| `Optical_Depth_047` | adim. (×0.001) | **SÍ** | AOD a 470 nm. Principal proxy de PM2.5 en superficie. Variable primaria (situacion1.md: *"AOD proxy PM"*). |
| `Optical_Depth_055` | adim. (×0.001) | **SÍ** | AOD a 550 nm. Banda de referencia internacional (AERONET). Permite validación cruzada. |
| `AOD_Uncertainty` | adim. (×0.0001) | **SÍ** | Incertidumbre del retrieval. Necesaria para ponderación estadística en el panel longitudinal. |
| `AOD_QA` | bitmask | **SÍ** | Calidad multidimensional (nubes, nieve, adyacencia). Filtra solo píxeles "Best quality" (bits 8-11 = 0). |
| `Column_WV` | cm (×0.001) | No | Redundante con ERA5 dewpoint y Sentinel-2 B9. |
| `FineModeFraction` | adim. | No | Solo válida sobre océano y grandes lagos. AOI de Cali es terrestre. |
| `Injection_Height` | m | No | Altura de inyección de humo. No es variable principal del panel. |
| `AngstromExp_470-780` | adim. | No | Solo válida sobre océano. |
| Ángulos (cosSZA, cosVZA, RelAZ, Scattering_Angle, Glint_Angle) | — | No | Metadatos de geometría de observación. |

---

## 3. Estimación de Pesos — AOI vs Tile Completo

### 3.1 Con AOI recortado (619 km²)

| Dataset | Píxeles AOI | MB/imagen | N° imgs | Total GB |
|---|---|---|---|---|
| S5P NO₂ | 20 × 25 | 0.01 | 40,064 | 0.36 |
| S5P SO₂ | 20 × 25 | 0.01 | 38,176 | 0.28 |
| S5P O₃ | 20 × 25 | 0.01 | 38,876 | 0.20 |
| Sentinel-2 SR | 2227 × 2783 | 113.5 | 1,136 | **125.9** |
| ERA5-Land | 2 × 3 | < 0.01 | 72,850 | 0.01 |
| MODIS AOD | 23 × 28 | 0.01 | 245,155 | 3.06 |
| **Total comprimido** | | | | **~130 GB** |
| **Total sin comprimir** | | | | **~325 GB** |

### 3.2 Con tile MGRS completo para Sentinel-2 (estrategia 626 GB)

El AOI cae en el tile MGRS **18NVK** (100 × 100 km). Exportar el tile completo:

| Elemento | Valor |
|---|---|
| Píxeles @ 10m | 10,000 × 10,000 = 100 M por banda |
| Tamaño estimado por escena (COG comprimido) | ~550 MB |
| Escenas disponibles | 1,136 |
| **S2 tiles completos** | **~620 GB** |
| + otros datasets (AOI) | + ~4 GB |
| **Total estimado** | **~624 GB ✓** |

---

## 4. Decisión de Formato: ¿Zarr directo vs GeoTIFF en HuggingFace?

### Contexto del pipeline

GEE expone los datos como `ImageCollection`. El servidor de descarga es `192.241.132.222` (SSH). El destino final es HuggingFace Hub como dataset público.

### Opción A — GeoTIFF COG → HuggingFace (raw)

**Pipeline:** GEE Export Task → GCS → rsync al servidor → HF upload

- Pros: proceso simple, estándar geoespacial, máxima compatibilidad
- Contras: archivos grandes (550 MB/escena S2), descarga completa obligatoria para cualquier análisis, sin chunking temporal nativo
- Resultado HF: colección de archivos, no un dataset streameable

### Opción B — GEE API (xee) → Zarr → HuggingFace ✅ RECOMENDADA

**Pipeline:** GEE ImageCollection → `xee` (xarray lazy) → `.to_zarr()` en servidor → HF upload

**¿Qué es `xee`?** Librería oficial de Google que envuelve una `ImageCollection` como `xr.Dataset` sin descargar nada. Se puede leer en chunks y escribir directamente a Zarr.

```python
import xarray as xr
import xee

ds = xr.open_dataset(
    "COPERNICUS/S2_SR_HARMONIZED",
    engine="ee",
    geometry=aoi,
    crs="EPSG:32618",
    scale=10
)
ds[bands_selected].to_zarr("/data/cali/sentinel2.zarr", mode="w")
```

**Ventajas frente a GeoTIFF:**

| Criterio | GeoTIFF COG | Zarr |
|---|---|---|
| Chunking temporal | No | Sí (configurable por tiempo + espacio) |
| Lectura parcial sin descarga total | Limitada | Nativa |
| Compresión | DEFLATE ~40% | Blosc/Zstd ~55-65% |
| Compatible xarray/dask | Con rasterio + overhead | Nativo |
| EDA streaming desde HF | No (descarga por archivo) | Sí (`xr.open_zarr("hf://...")`) |
| Trazabilidad de metadatos | Por archivo | Atributos Zarr en `.zattrs` |
| Conversión posterior | Requiere paso extra | Listo para ML |

**EDA desde HuggingFace con Zarr:**

```python
import xarray as xr
ds = xr.open_zarr("hf://datasets/org/panel-cali-longitudinal/sentinel2.zarr")
ds.sel(time="2022-06").mean("time").plot()  # sin descargar los 620 GB
```

**Zarr es mejor para el proyecto porque:**
1. El panel es longitudinal → el eje temporal es el acceso principal. Zarr chunkeado por tiempo permite leer un mes sin tocar el resto.
2. EDA sin descarga total: cualquier colaborador puede explorar desde HF con xarray.
3. Trazabilidad embebida: los atributos Zarr (`.zattrs`) guardan collection_id, fechas, bandas seleccionadas, versión GEE → trazabilidad a nivel de dataset.
4. Elimina el paso intermedio GeoTIFF → ahorra ~620 GB de almacenamiento temporal en el servidor.
5. Compresión superior: ~55-65% vs ~40% GeoTIFF DEFLATE → el dataset en HF ocupa menos.

**Consideración de batching para 620 GB:** `xee` requiere batching para datasets grandes. El servidor SSH maneja esto con chunks de tiempo (ej. 1 mes por job).

---

## 5. Estructura Zarr Recomendada en HuggingFace

```
panel-cali-longitudinal/
├── sentinel2.zarr/          # (time: 1136, band: 15, y: 10000, x: 10000) uint16 @ 10m equiv.
├── sentinel5p_no2.zarr/     # (time: 40064, y: 25, x: 20) float32
├── sentinel5p_so2.zarr/     # (time: 38176, y: 25, x: 20) float32
├── sentinel5p_o3.zarr/      # (time: 38876, y: 25, x: 20) float32
├── era5_land.zarr/          # (time: 72850, variable: 6, y: 3, x: 2) float32
├── era5_blh.zarr/           # (time: ~72850, y: 3, x: 2) float32  ← colección separada
└── modis_aod.zarr/          # (time: 245155, band: 4, y: 28, x: 23) float32
```

Cada `.zarr` lleva `.zattrs` con: `collection_id`, `start_date`, `end_date`, `bands_selected`, `crs`, `scale_m`, `aoi_bbox`, `gee_project`, `query_date`.

---

## 6. Períodos por Dataset

| Dataset | Período disponible | Período del proyecto | Razón |
|---|---|---|---|
| S5P NO₂ | 2018-06-28 → presente | **2018-07-01 → 2026-04-29** | Inicio real de datos completos |
| S5P SO₂ | 2018-12-05 → presente | **2019-01-01 → 2026-04-29** | Primeros meses con gaps; estabiliza en 2019 |
| S5P O₃ | 2018-09-08 → presente | **2018-09-08 → 2026-04-29** | Usar desde inicio disponible |
| Sentinel-2 SR | 2017-03-28 → presente | **2018-01-01 → 2026-04-29** | Consistencia con el panel longitudinal |
| ERA5-Land | 1950-01-01 → presente | **2018-01-01 → 2026-04-29** | Alineado con observaciones satelitales |
| ERA5 BLH | 1940-01-01 → presente | **2018-01-01 → 2026-04-29** | Alineado con el panel |
| MODIS AOD | 2000-02-24 → presente | **2018-01-01 → 2026-04-29** | Consistencia temporal del panel |

---

## 7. Resumen Ejecutivo

| Pregunta | Respuesta |
|---|---|
| ¿Imágenes S2 disponibles (2018-2026)? | **1,136 escenas** |
| ¿Peso AOI recortado (comprimido)? | **~130 GB** |
| ¿Peso AOI sin comprimir? | **~325 GB** |
| ¿Se alcanzan 626 GB con AOI recortado? | **No** |
| ¿Cómo alcanzar 626 GB? | Exportar **tile MGRS 18NVK completo** (100×100 km) → ~620 GB solo S2 |
| ¿Formato de subida a HF? | **Zarr** vía `xee` (pipeline directo sin GeoTIFF intermedio) |
| ¿Por qué Zarr sobre GeoTIFF? | Chunking temporal, EDA streaming, compresión superior, trazabilidad en `.zattrs` |
| ¿BLH disponible en ERA5-Land? | **No** — error del enunciado; BLH es de ERA5 atmosférico. Documentado, no se agrega nueva colección. |
| ¿EDA posible sin descargar? | **Sí** — directamente vía GEE/`geemap` (server-side) o streaming desde HF con `xr.open_zarr("hf://...")` |
| ¿Factible en servidor SSH? | **Sí** — `gee_to_zarr.py` usa xee → zarr → upload HF con logs en `/data/cali/logs/` |
