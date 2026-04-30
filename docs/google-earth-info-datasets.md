# Datasets de Google Earth Engine - Referencia

## 1. NO2 Sentinel-5P (Dióxido de Nitrógeno)

- **ID:** `COPERNICUS/S5P/OFFL/L3_NO2`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2
- **Resolución espacial:** 1113.2 m (todos las bandas)
- **Resolución temporal:** 2 días (revisit interval)
- **Disponibilidad:** 2018-06-28 a 2026-04-20
- **Productor:** European Union/ESA/Copernicus
- **Descripción:** Datos offline de alta resolución de concentraciones de NO2. Los óxidos de nitrógeno entran a la atmósfera por actividades antropogénicas (combustión fósil, quema de biomasa) y procesos naturales (incendios, rayos). El sistema de procesamiento TROPOMI usa el modelo de transporte químico TM5-MP a resolución de 1x1 grado.

### Bandas

| Nombre | Unidades | Descripción |
|---|---|---|
| `NO2_column_number_density` | mol/m^2 | Columna vertical total de NO2 |
| `tropospheric_NO2_column_number_density` | mol/m^2 | Columna vertical troposférica de NO2 |
| `stratospheric_NO2_column_number_density` | mol/m^2 | Columna vertical estratosférica de NO2 |
| `NO2_slant_column_number_density` | mol/m^2 | Densidad de columna inclinada de NO2 |
| `tropopause_pressure` | Pa | Presión de tropopausa |
| `absorbing_aerosol_index` | Adimensional | Índice de aerosoles (354/388 nm) |
| `cloud_fraction` | Fracción | Fracción de nube efectiva |
| `sensor_altitude` | m | Altitud del satélite |
| `sensor_azimuth_angle` | deg | Ángulo acimutal del satélite |
| `sensor_zenith_angle` | deg | Ángulo cenital del satélite |
| `solar_azimuth_angle` | deg | Ángulo acimutal del Sol |
| `solar_zenith_angle` | deg | Ángulo cenital del Sol |

---

## 2. SO2 Sentinel-5P (Dióxido de Azufre)

- **ID:** `COPERNICUS/S5P/OFFL/L3_SO2`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_SO2
- **Resolución espacial:** 1113.2 m (todos las bandas)
- **Resolución temporal:** 2 días (revisit interval)
- **Disponibilidad:** 2018-12-05 a 2026-04-26
- **Productor:** European Union/ESA/Copernicus
- **Descripción:** Datos offline de concentraciones atmosféricas de SO2. Aproximadamente el 30% del SO2 emitido proviene de fuentes naturales; la mayoría es de origen antropogénico. El SO2 afecta la calidad del aire, la salud humana y el clima a través de la formación de aerosoles sulfatados. Las emisiones volcánicas de SO2 también representan una amenaza para la aviación.

### Bandas

| Nombre | Unidades | Descripción |
|---|---|---|
| `SO2_column_number_density` | mol/m^2 | Densidad de columna vertical de SO2 a nivel del suelo |
| `SO2_column_number_density_amf` | mol/m^2 | Factor de masa de aire promedio ponderado |
| `SO2_slant_column_number_density` | mol/m^2 | Densidad de columna inclinada corregida por anillo |
| `absorbing_aerosol_index` | Adimensional | Índice de aerosoles absorbentes (340/380 nm) |
| `cloud_fraction` | Fracción | Fracción de nube efectiva |
| `sensor_azimuth_angle` | deg | Ángulo acimutal del satélite |
| `sensor_zenith_angle` | deg | Ángulo cenital del satélite |
| `solar_azimuth_angle` | deg | Ángulo acimutal del Sol |
| `solar_zenith_angle` | deg | Ángulo cenital del Sol |
| `SO2_column_number_density_15km` | mol/m^2 | Densidad de columna vertical de SO2 a 15km |

### Notas de calidad

Filtros QA aplicados antes de harpconvert:
- `snow_ice < 0.5`
- `sulfurdioxide_total_air_mass_factor_polluted > 0.1`
- `sulfurdioxide_total_vertical_column > -0.001`
- `qa_value > 0.5`
- `cloud_fraction_crb < 0.3`
- `solar_zenith_angle < 60`
- La banda de 15km solo se ingiere cuando `solar_zenith_angle < 70`

---

## 3. O3 Sentinel-5P (Ozono)

- **ID:** `COPERNICUS/S5P/OFFL/L3_O3`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_O3
- **Resolución espacial:** 1113.2 m (todos las bandas)
- **Resolución temporal:** 2 días (revisit interval)
- **Disponibilidad:** 2018-09-08 a 2026-04-26
- **Productor:** European Union/ESA/Copernicus
- **Descripción:** Datos offline de concentraciones de columna total de ozono. En la estratosfera, la capa de ozono protege contra la radiación UV peligrosa. En la troposfera, actúa como agente de limpieza pero a altas concentraciones es perjudicial para la salud humana, animales y vegetación. También es un importante gas de efecto invernadero. Existe también el producto `COPERNICUS/S5P/OFFL/L3_O3_TCL` para la columna troposférica. Se usa el algoritmo GODFIT para los productos offline.

### Bandas

| Nombre | Unidades | Descripción |
|---|---|---|
| `O3_column_number_density` | mol/m^2 | Columna atmosférica total de O3 (algoritmo GODfit) |
| `O3_effective_temperature` | K | Temperatura efectiva de la sección transversal de ozono |
| `cloud_fraction` | Fracción | Fracción de nube efectiva |
| `sensor_azimuth_angle` | deg | Ángulo acimutal del satélite |
| `sensor_zenith_angle` | deg | Ángulo cenital del satélite |
| `solar_azimuth_angle` | deg | Ángulo acimutal del Sol |
| `solar_zenith_angle` | deg | Ángulo cenital del Sol |

### Notas de calidad

Filtros QA aplicados antes de harpconvert:
- `ozone_total_vertical_column` en [0, 0.45]
- `ozone_effective_temperature` en [180, 260]
- `ring_scale_factor` en [0, 0.15]
- `effective_albedo` en [-0.5, 1.5]

---

## 4. Sentinel-2 MSI Level-2A (Superficie - Harmonized)

- **ID:** `COPERNICUS/S2_SR_HARMONIZED`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
- **Resolución espacial:** 10 m / 20 m / 60 m (varía por banda)
- **Resolución temporal:** 5 días (revisit interval)
- **Disponibilidad:** 2017-03-28 a 2026-04-29
- **Productor:** European Union/ESA/Copernicus
- **Descripción:** Imágenes multiespectrales de amplia cobertura y alta resolución para monitoreo terrestre (vegetación, suelo, agua, vías navegables interiores y zonas costeras). Los datos L2 se descargan de CDSE y se calculan con sen2cor. A partir del 2022-01-25, las escenas con `PROCESSING_BASELINE >= '04.00'` tienen un desplazamiento de +1000 en el rango DN; la colección HARMONIZED ajusta esto para mantener consistencia con escenas anteriores. Los valores de reflectancia están escalados por 0.0001 (dividir entre 10000).

### Bandas espectrales

| Banda | Resolución | Longitud de onda (S2A / S2B) | Descripción |
|---|---|---|---|
| `B1` | 60 m | 443.9nm / 442.3nm | Aerosoles |
| `B2` | 10 m | 496.6nm / 492.1nm | Azul |
| `B3` | 10 m | 560nm / 559nm | Verde |
| `B4` | 10 m | 664.5nm / 665nm | Rojo |
| `B5` | 20 m | 703.9nm / 703.8nm | Red Edge 1 |
| `B6` | 20 m | 740.2nm / 739.1nm | Red Edge 2 |
| `B7` | 20 m | 782.5nm / 779.7nm | Red Edge 3 |
| `B8` | 10 m | 835.1nm / 833nm | NIR |
| `B8A` | 20 m | 864.8nm / 864nm | Red Edge 4 |
| `B9` | 60 m | 945nm / 943.2nm | Vapor de agua |
| `B11` | 20 m | 1613.7nm / 1610.4nm | SWIR 1 |
| `B12` | 20 m | 2202.4nm / 2185.7nm | SWIR 2 |

### Bandas adicionales L2

| Nombre | Resolución | Descripción |
|---|---|---|
| `AOT` | 10 m | Espesor óptico de aerosoles (escala 0.001) |
| `WVP` | 10 m | Presión de vapor de agua en cm (escala 0.001) |
| `SCL` | 20 m | Mapa de clasificación de escena (valores 1-11) |
| `TCI_R`, `TCI_G`, `TCI_B` | 10 m | Canales RGB de imagen en color verdadero |
| `MSK_CLDPRB` | 20 m | Mapa de probabilidad de nubes (0-100) |
| `MSK_SNWPRB` | 10 m | Mapa de probabilidad de nieve (0-100) |
| `QA60` | 60 m | Máscara de nubes (bit 10: nubes opacas, bit 11: cirrus) |

### Filtro de nubes usado en el proyecto

```python
.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
```

---

## 5. ERA5-Land Hourly (Reanálisis Climático ECMWF)

- **ID:** `ECMWF/ERA5_LAND/HOURLY`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY
- **Resolución espacial:** 11132 m (~11 km)
- **Resolución temporal:** 1 hora
- **Disponibilidad:** 1950-01-01 a 2026-04-21
- **Productor:** Copernicus Climate Data Store / ECMWF
- **Descripción:** Dataset de reanálisis que proporciona una vista consistente de la evolución de variables terrestres a resolución mejorada respecto a ERA5. Combina datos de modelo con observaciones de todo el mundo. Incluye 50+ variables de temperatura, humedad del suelo, nieve, lagos, radiación, flujos de calor, evaporación, escorrentía, viento y precipitación.

### Bandas principales (selección)

| Nombre | Unidades | Descripción |
|---|---|---|
| `temperature_2m` | K | Temperatura del aire a 2m sobre la superficie |
| `dewpoint_temperature_2m` | K | Temperatura de punto de rocío a 2m |
| `skin_temperature` | K | Temperatura de la superficie |
| `soil_temperature_level_1` | K | Temperatura del suelo capa 1 (0-7 cm) |
| `soil_temperature_level_2` | K | Temperatura del suelo capa 2 (7-28 cm) |
| `soil_temperature_level_3` | K | Temperatura del suelo capa 3 (28-100 cm) |
| `soil_temperature_level_4` | K | Temperatura del suelo capa 4 (100-289 cm) |
| `volumetric_soil_water_layer_1` | Fracción | Agua volumétrica del suelo capa 1 (0-7 cm) |
| `volumetric_soil_water_layer_2` | Fracción | Agua volumétrica del suelo capa 2 (7-28 cm) |
| `volumetric_soil_water_layer_3` | Fracción | Agua volumétrica del suelo capa 3 (28-100 cm) |
| `volumetric_soil_water_layer_4` | Fracción | Agua volumétrica del suelo capa 4 (100-289 cm) |
| `total_precipitation` | m | Precipitación total acumulada (lluvia + nieve) |
| `total_precipitation_hourly` | m | Precipitación total desagregada a valores horarios |
| `surface_pressure` | Pa | Presión superficial |
| `u_component_of_wind_10m` | m/s | Componente zonal del viento a 10m |
| `v_component_of_wind_10m` | m/s | Componente meridional del viento a 10m |
| `surface_net_solar_radiation` | J/m^2 | Radiación solar neta superficial (acumulada) |
| `surface_net_solar_radiation_hourly` | J/m^2 | Radiación solar neta superficial (horaria) |
| `surface_solar_radiation_downwards` | J/m^2 | Radiación solar descendente superficial (acum.) |
| `surface_solar_radiation_downwards_hourly` | J/m^2 | Radiación solar descendente superficial (horaria) |
| `snow_depth` | m | Profundidad de nieve |
| `snow_cover` | Fracción | Fracción de celda cubierta por nieve |
| `total_evaporation` | m eq. agua | Evaporación total acumulada |
| `total_evaporation_hourly` | m eq. agua | Evaporación total horaria |
| `runoff` | m | Escorrentía total acumulada |
| `runoff_hourly` | m | Escorrentía total horaria |
| `forecast_albedo` | Adimensional | Albedo de la superficie |

### Notas importantes

- Las variables acumuladas se reinician a medianoche diariamente
- Earth Engine proporciona 19 bandas adicionales `_hourly` calculadas como la diferencia entre pasos de pronóstico consecutivos
- **Problema conocido:** Los valores de 3 componentes de evapotranspiración están intercambiados (ver documentación)
- Requiere atribución: *"Generated using Copernicus Climate Change Service Information [Year]"*

### Cita

> Muñoz Sabater, J., (2019): ERA5-Land monthly averaged data from 1981 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). doi:10.24381/cds.68d2bb30

---

## 6. MODIS MCD19A2 (Aerosol Optical Depth - MAIAC)

- **ID:** `MODIS/061/MCD19A2_GRANULES`
- **Enlace:** https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD19A2_GRANULES
- **Resolución espacial:** 1000 m (1 km)
- **Resolución temporal:** 1 día
- **Disponibilidad:** 2000-02-24 a 2026-04-24
- **Productor:** NASA LP DAAC at USGS EROS Center
- **DOI:** https://doi.org/10.5067/MODIS/MCD19A2.061
- **Descripción:** Producto diario combinado Terra+Aqua de Profundidad Óptica de Aerosoles (AOD) terrestre a 1 km de resolución usando el algoritmo MAIAC (Multi-angle Implementation of Atmospheric Correction).

### Bandas

| Nombre | Unidades | Escala | Descripción |
|---|---|---|---|
| `Optical_Depth_047` | Adimensional | 0.001 | AOD terrestre en banda azul MODIS (0.47 μm) |
| `Optical_Depth_055` | Adimensional | 0.001 | AOD terrestre en banda verde MODIS (0.55 μm) |
| `AOD_Uncertainty` | Adimensional | 0.0001 | Incertidumbre del AOD basada en brillo superficial |
| `FineModeFraction` | Adimensional | - | Fracción de modo fino (océano y grandes lagos) |
| `Column_WV` | cm | 0.001 | Columna de vapor de agua sobre tierra |
| `AOD_QA` | - | - | Máscara de calidad del AOD (ver bitmask) |
| `Injection_Height` | m | - | Altura de inyección de humo |
| `AngstromExp_470-780` | Adimensional | 0.0001 | Exponente de Ångström 470-780nm sobre océano |
| `cosSZA` | Adimensional | 0.0001 | Coseno del ángulo cenital solar (5 km) |
| `cosVZA` | Adimensional | 0.0001 | Coseno del ángulo cenital de vista (5 km) |
| `RelAZ` | deg | 0.01 | Ángulo acimutal relativo (5 km) |
| `Scattering_Angle` | deg | 0.01 | Ángulo de dispersión (5 km) |
| `Glint_Angle` | deg | 0.01 | Ángulo de brillo especular |

### Bitmask AOD_QA

| Bits | Campo | Valores |
|---|---|---|
| 0-2 | Cloud mask | 0=Undefined, 1=Clear, 2=Possibly cloudy, 3=Cloudy, 5=Cloud shadow, 6=Hot spot, 7=Water sediments |
| 3-4 | Land/water/snow/ice | 0=Land, 1=Water, 2=Snow, 3=Ice |
| 5-7 | Adjacency mask | 0=Clear, 1=Adjacent to clouds, 2=>4 cloudy pixels, 3=1 cloudy neighbor, 4=Adjacent to snow, 5=Snow detected |
| 8-11 | QA for AOD | 0=Best quality, 5=No retrieval, etc. |
| 12 | Glint mask | 0=No glint, 1=Glint |
| 13-14 | Aerosol model | 0=Background, 1=Smoke, 2=Dust |

### Notas

- Los datos MODIS LP DAAC no tienen restricciones de uso, venta o redistribución
- AOD no se recupera en altitudes > 4.2 km excepto cuando se detecta humo o polvo (se reporta 0.02 estático)

---

## Resumen Comparativo de los Datasets

| Dataset | Resolución espacial | Resolución temporal | Bandas | Disponibilidad | Uso en el proyecto |
|---|---|---|---|---|---|
| S5P NO2 | 1113.2 m | 2 días | ~12 | 2018-06 a 2026-04 | Contaminación por NO2 |
| S5P SO2 | 1113.2 m | 2 días | ~10 | 2018-12 a 2026-04 | Contaminación por SO2 |
| S5P O3 | 1113.2 m | ~7 | 2018-09 a 2026-04 | Ozono total | |
| Sentinel-2 SR | 10/20/60 m | 5 días | ~24 | 2017-03 a 2026-04 | Reflectancia superficial (NDVI, etc.) |
| ERA5-Land | 11132 m | 1 hora | ~50 | 1950-01 a 2026-04 | Variables meteorológicas |
| MODIS MCD19A2 | 1000 m | 1 día | ~12 | 2000-02 a 2026-04 | Aerosoles (AOD) |