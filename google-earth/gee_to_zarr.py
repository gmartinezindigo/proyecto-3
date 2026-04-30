import ee
import json
import logging
import os
import xarray as xr
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import HfApi

load_dotenv()

GEE_PROJECT = "charming-mile-436804-q2"
HF_TOKEN    = os.environ["HF_TOKEN"]
HF_DATASET  = os.environ["DATASET"].lstrip("/")
OUTPUT_DIR  = Path("/data/cali/zarr")
LOG_DIR     = Path("/data/cali/logs")
GB_ALERT    = 50

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"{run_id}.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger()

ee.Initialize(project=GEE_PROJECT)
api = HfApi(token=HF_TOKEN)

AOI = ee.Geometry.Rectangle([-76.60, 3.30, -76.40, 3.55])
CRS = "EPSG:32618"

DATASETS = [
    {
        "name": "sentinel5p_no2",
        "collection": "COPERNICUS/S5P/OFFL/L3_NO2",
        "start": "2018-07-01", "end": "2026-04-29",
        "scale": 1113.2,
        "bands": ["tropospheric_NO2_column_number_density", "cloud_fraction"],
    },
    {
        "name": "sentinel5p_so2",
        "collection": "COPERNICUS/S5P/OFFL/L3_SO2",
        "start": "2019-01-01", "end": "2026-04-29",
        "scale": 1113.2,
        "bands": ["SO2_column_number_density", "cloud_fraction"],
    },
    {
        "name": "sentinel5p_o3",
        "collection": "COPERNICUS/S5P/OFFL/L3_O3",
        "start": "2018-09-08", "end": "2026-04-29",
        "scale": 1113.2,
        "bands": ["O3_column_number_density", "cloud_fraction"],
    },
    {
        "name": "sentinel2_sr",
        "collection": "COPERNICUS/S2_SR_HARMONIZED",
        "start": "2018-01-01", "end": "2026-04-29",
        "scale": 10.0,
        "bands": ["B1","B2","B3","B4","B5","B6","B7","B8","B8A","B9","B11","B12","AOT","SCL","QA60"],
    },
    {
        "name": "era5_land",
        "collection": "ECMWF/ERA5_LAND/HOURLY",
        "start": "2018-01-01", "end": "2026-04-29",
        "scale": 11132.0,
        "bands": [
            "temperature_2m", "dewpoint_temperature_2m",
            "u_component_of_wind_10m", "v_component_of_wind_10m",
            "surface_pressure", "total_precipitation_hourly",
        ],
    },
    {
        "name": "modis_aod",
        "collection": "MODIS/061/MCD19A2_GRANULES",
        "start": "2018-01-01", "end": "2026-04-29",
        "scale": 1000.0,
        "bands": ["Optical_Depth_047", "Optical_Depth_055", "AOD_Uncertainty", "AOD_QA"],
    },
]


def dir_size_gb(path: Path) -> float:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1024 ** 3


def process(cfg: dict) -> dict:
    out = OUTPUT_DIR / f'{cfg["name"]}.zarr'

    col = (
        ee.ImageCollection(cfg["collection"])
        .filterDate(cfg["start"], cfg["end"])
        .filterBounds(AOI)
        .select(cfg["bands"])
    )

    ds = xr.open_dataset(col, engine="ee", geometry=AOI, crs=CRS, scale=cfg["scale"])
    ds.chunk({"time": 50, "X": 256, "Y": 256}).to_zarr(out, mode="w", consolidated=True)

    size = dir_size_gb(out)
    alert = size > GB_ALERT
    log.info(f'{cfg["name"]} → {size:.3f} GB{"  ⚠ supera {GB_ALERT} GB" if alert else ""}')
    return {"zarr": str(out), "size_gb": round(size, 3), "large_file_alert": alert}


record = {
    "run_id":   run_id,
    "started":  datetime.now(timezone.utc).isoformat(),
    "datasets": {},
}

for cfg in DATASETS:
    log.info(f'Iniciando {cfg["name"]}')
    try:
        result = {"status": "ok", **process(cfg)}
    except Exception as exc:
        log.error(f'{cfg["name"]} falló: {exc}')
        result = {"status": "error", "error": str(exc)}
    record["datasets"][cfg["name"]] = result

record["total_gb"]   = round(sum(r.get("size_gb", 0) for r in record["datasets"].values()), 3)
record["completed"]  = datetime.now(timezone.utc).isoformat()

json_path = LOG_DIR / f"{run_id}.json"
json_path.write_text(json.dumps(record, indent=2))
log.info(f'Total acumulado: {record["total_gb"]:.3f} GB  |  Registro: {json_path}')

for cfg in DATASETS:
    if record["datasets"].get(cfg["name"], {}).get("status") != "ok":
        continue
    zarr_path = OUTPUT_DIR / f'{cfg["name"]}.zarr'
    log.info(f'Subiendo {cfg["name"]} a HuggingFace ({HF_DATASET})')
    api.upload_large_folder(
        folder_path=str(zarr_path),
        repo_id=HF_DATASET,
        repo_type="dataset",
        path_in_repo=f'{cfg["name"]}.zarr',
    )
    log.info(f'{cfg["name"]} subido correctamente')
