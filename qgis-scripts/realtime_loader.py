# realtime_loader.py
# Load earthquake events from CSV into QGIS, keeping only last 48h

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsFields,
    QgsField,
    QgsMemoryProviderUtils,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem,
    QgsVectorDataProvider
)
from PyQt5.QtCore import QVariant
import csv
from datetime import datetime, timedelta

# === Settings ===
CSV_PATH = "earthquakes_grassgis.csv"
LAYER_NAME = "Real-time Earthquakes"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
MAX_AGE_HOURS = 48

# === Initialize Layer ===
existing_layer = QgsProject.instance().mapLayersByName(LAYER_NAME)
if existing_layer:
    memory_layer = existing_layer[0]
    memory_layer.dataProvider().truncate()  # Clear existing features
else:
    memory_layer = QgsVectorLayer("Point?crs=EPSG:4326", LAYER_NAME, "memory")
    provider = memory_layer.dataProvider()
    provider.addAttributes([
        QgsField("time", QVariant.String),
        QgsField("latitude", QVariant.Double),
        QgsField("longitude", QVariant.Double),
        QgsField("magnitude", QVariant.Double),
        QgsField("region", QVariant.String),
        QgsField("unid", QVariant.String),
    ])
    memory_layer.updateFields()
    QgsProject.instance().addMapLayer(memory_layer)

# === Helper ===
def is_recent(timestamp_str):
    try:
        event_time = datetime.strptime(timestamp_str, TIME_FORMAT)
        return datetime.utcnow() - event_time <= timedelta(hours=MAX_AGE_HOURS)
    except Exception:
        return False

# === Load CSV and Filter ===
unid_set = set()
features = []

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not is_recent(row["time"]):
            continue
        if row["unid"] in unid_set:
            continue
        unid_set.add(row["unid"])

        point = QgsPointXY(float(row["longitude"]), float(row["latitude"]))
        geom = QgsGeometry.fromPointXY(point)

        feat = QgsFeature()
        feat.setGeometry(geom)
        feat.setAttributes([
            row["time"],
            float(row["latitude"]),
            float(row["longitude"]),
            float(row["magnitude"]),
            row["region"],
            row["unid"]
        ])
        features.append(feat)

memory_layer.dataProvider().addFeatures(features)
memory_layer.updateExtents()
print(f"✅ Loaded {len(features)} recent earthquake events.")
