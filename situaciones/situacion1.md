# Situación 1: Panel Analítico Longitudinal

## Descripción del Requerimiento

Se requiere construir un panel analítico longitudinal de mínimo 50 GB que integre 5 años de imágenes satelitales sobre el área metropolitana de Santiago de Cali.

**Coordenadas de interés:**
- Latitud: 3.30°N a 3.55°N
- Longitud: -76.60°W a -76.40°W

**Áreas incluidas:**
- Corredor industrial Yumbo—Acopi
- Zona de cultivos de caña del norte del Valle

El panel debe permitir el estudio conjunto de:
1. Columnas troposféricas de NO₂, SO₂ y O₃ provenientes de Sentinel-5P TROPOMI.
2. Covariables ópticas de alta resolución provenientes de Sentinel-2 MSI.
3. Covariables meteorológicas de reanálisis ERA5-Land.
4. *Ground truth* puntual de las estaciones del DAGMA y los reportes SISAIRE.

---

## Fuentes de Datos Satelitales y Meteorológicos

| Fuente / Producto | Variable / Medida | Resolución Espacial | Resolución Temporal | Plataforma / Acceso |
| :--- | :--- | :--- | :--- | :--- |
| **Sentinel-5P L2 OFFL** | NO₂ troposférico | 3.5 × 5.5 km | Diaria (1—2 órbitas) | Copernicus DataSpace · GEE |
| **Sentinel-5P L2 OFFL** | SO₂ vertical column | 3.5 × 5.5 km | Diaria | Copernicus DataSpace · GEE |
| **Sentinel-5P L2 OFFL** | O₃ total column | 3.5 × 5.5 km | Diaria | Copernicus DataSpace · GEE |
| **Sentinel-2 L2A** | 13 bandas (B2-B12)* | 10 / 20 / 60 m | 5 días | Copernicus · GEE |
| **MODIS MCD19A2** | AOD (proxy PM) | 1 km | Diaria | NASA Earthdata · GEE |
| **ERA5-Land** | T2m, viento, BLH, RH | 9 km | Horaria | Copernicus CDS · GEE |

*\* Requiere selección de bandas necesarias para Sentinel-2.*
