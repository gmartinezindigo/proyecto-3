import ee
import json
import math
from datetime import datetime

ee.Initialize(project='charming-mile-436804-q2')

AOI_COORDS = [-76.60, 3.30, -76.40, 3.55]
AOI = ee.Geometry.Rectangle(AOI_COORDS)

AOI_W_DEG = 0.20
AOI_H_DEG = 0.25
AOI_W_KM  = AOI_W_DEG * 111.32
AOI_H_KM  = AOI_H_DEG * 111.32
AOI_AREA_KM2 = AOI_W_KM * AOI_H_KM

COLLECTIONS = {
    'sentinel5p_no2': {
        'collection_id': 'COPERNICUS/S5P/OFFL/L3_NO2',
        'start': '2018-06-28',
        'end':   '2026-04-29',
        'resolution_m': 1113.2,
        'n_bands_total': 12,
        'bytes_per_value': 4,
    },
    'sentinel5p_so2': {
        'collection_id': 'COPERNICUS/S5P/OFFL/L3_SO2',
        'start': '2018-12-05',
        'end':   '2026-04-29',
        'resolution_m': 1113.2,
        'n_bands_total': 10,
        'bytes_per_value': 4,
    },
    'sentinel5p_o3': {
        'collection_id': 'COPERNICUS/S5P/OFFL/L3_O3',
        'start': '2018-09-08',
        'end':   '2026-04-29',
        'resolution_m': 1113.2,
        'n_bands_total': 7,
        'bytes_per_value': 4,
    },
    'sentinel2_sr': {
        'collection_id': 'COPERNICUS/S2_SR_HARMONIZED',
        'start': '2018-01-01',
        'end':   '2026-04-29',
        'resolution_m': 10.0,
        'n_bands_total': 24,
        'bytes_per_value': 2,
    },
    'era5_land': {
        'collection_id': 'ECMWF/ERA5_LAND/HOURLY',
        'start': '2018-01-01',
        'end':   '2026-04-29',
        'resolution_m': 11132.0,
        'n_bands_total': 8,
        'bytes_per_value': 4,
    },
    'modis_aod': {
        'collection_id': 'MODIS/061/MCD19A2_GRANULES',
        'start': '2018-01-01',
        'end':   '2026-04-29',
        'resolution_m': 1000.0,
        'n_bands_total': 13,
        'bytes_per_value': 4,
    },
}

COMPRESSION_FACTOR = 0.4  # GeoTIFF DEFLATE típico


def pixel_dims(res_m):
    w = math.ceil((AOI_W_DEG * 111320) / res_m)
    h = math.ceil((AOI_H_DEG * 111320) / res_m)
    return w, h, w * h


def size_mb(n_pixels, n_bands, bytes_per_val, compression=COMPRESSION_FACTOR):
    return (n_pixels * n_bands * bytes_per_val * compression) / (1024 ** 2)


def query_and_build():
    results = {}

    for key, cfg in COLLECTIONS.items():
        col = (
            ee.ImageCollection(cfg['collection_id'])
            .filterDate(cfg['start'], cfg['end'])
            .filterBounds(AOI)
        )
        n_images = col.size().getInfo()

        w, h, n_pixels = pixel_dims(cfg['resolution_m'])
        mb_per_image = size_mb(n_pixels, cfg['n_bands_total'], cfg['bytes_per_value'])
        total_gb_aoi  = (n_images * mb_per_image) / 1024

        results[key] = {
            **cfg,
            'n_images':      n_images,
            'aoi_pixels_w':  w,
            'aoi_pixels_h':  h,
            'aoi_n_pixels':  n_pixels,
            'mb_per_image_compressed':  round(mb_per_image, 4),
            'total_gb_aoi_compressed':  round(total_gb_aoi, 4),
        }
        print(f"{key}: {n_images:,} imgs → {total_gb_aoi:.2f} GB")

    total_aoi_gb = sum(r['total_gb_aoi_compressed'] for r in results.values())

    output = {
        'metadata': {
            'query_date':      datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'gee_project':     'charming-mile-436804-q2',
            'aoi_bbox':        {'xmin': AOI_COORDS[0], 'ymin': AOI_COORDS[1],
                                'xmax': AOI_COORDS[2], 'ymax': AOI_COORDS[3]},
            'aoi_area_km2':    round(AOI_AREA_KM2, 2),
            'aoi_dimensions':  {'width_km': round(AOI_W_KM, 2), 'height_km': round(AOI_H_KM, 2)},
            'compression_factor_assumed': COMPRESSION_FACTOR,
            'compression_format':         'GeoTIFF DEFLATE',
        },
        'datasets': results,
        'summary': {
            'total_images':           sum(r['n_images'] for r in results.values()),
            'total_gb_aoi_compressed': round(total_aoi_gb, 2),
            'total_gb_aoi_raw':        round(total_aoi_gb / COMPRESSION_FACTOR, 2),
            'target_min_gb':           626,
            'aoi_reaches_target':      total_aoi_gb >= 626,
            'strategy_to_reach_target': (
                'Export full MGRS tile 18NVK (100x100 km) for Sentinel-2 instead of AOI clip. '
                'S2 full tile: ~550 MB/scene × 1136 scenes = ~620 GB.'
            ),
        },
    }

    with open('docs/gee_query_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal AOI comprimido : {total_aoi_gb:.2f} GB")
    print(f"Total AOI sin comprimir: {total_aoi_gb / COMPRESSION_FACTOR:.2f} GB")
    print("Guardado en docs/gee_query_results.json")


if __name__ == '__main__':
    query_and_build()
