
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsMarkerSymbol,
    QgsSimpleMarkerSymbolLayer,
    QgsRuleBasedRenderer,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsVectorLayerSimpleLabeling,
    QgsProperty,
    QgsUnitTypes,
    edit
)
from qgis.PyQt.QtGui import QColor
from datetime import datetime, timedelta
import os

# Path to your CSV file
csv_path = os.path.join(os.path.dirname(__file__), 'earthquakes_grassgis.csv')

# Load the CSV as a point layer
uri = f"file://{csv_path}?delimiter=,&xField=longitude&yField=latitude&crs=EPSG:4326"
layer_name = "Earthquakes_Realtime"
existing_layer = QgsProject.instance().mapLayersByName(layer_name)

if existing_layer:
    QgsProject.instance().removeMapLayer(existing_layer[0])

vlayer = QgsVectorLayer(uri, layer_name, "delimitedtext")

if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)

    # Remove features older than 48 hours
    with edit(vlayer):
        for feat in vlayer.getFeatures():
            try:
                event_time = datetime.strptime(feat["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                if datetime.utcnow() - event_time > timedelta(hours=48):
                    vlayer.deleteFeature(feat.id())
            except:
                continue

    # Create geometry generator for circles
    symbol = QgsMarkerSymbol.createSimple({})
    geom_gen = QgsSimpleMarkerSymbolLayer()
    geom_gen.setShape(QgsSimpleMarkerSymbolLayer.Circle)

    # Set radius as exponential function of magnitude
    symbol.deleteSymbolLayer(0)
    symbol.appendSymbolLayer(geom_gen)
    symbol.setDataDefinedSize(
        QgsProperty.fromExpression("2^magnitude"),
        QgsUnitTypes.RenderMapUnits
    )

    # Define categorized colors
    root_rule = QgsRuleBasedRenderer.Rule(None)
    ranges = [
        (0, 2, 'green', 0.5),
        (2, 3, 'lightgreen', 0.6),
        (3, 4, 'yellow', 0.7),
        (4, 5, 'orange', 0.8),
        (5, 6, 'red', 0.9),
        (6, 10, 'darkred', 1.0)
    ]
    for min_mag, max_mag, color, opacity in ranges:
        rule = QgsRuleBasedRenderer.Rule(symbol.clone())
        rule.setLabel(f"{min_mag} - {max_mag}")
        rule.setFilterExpression(f"magnitude >= {min_mag} AND magnitude < {max_mag}")
        rule.symbol().setColor(QColor(color))
        rule.symbol().setOpacity(opacity)
        root_rule.appendChild(rule)

    renderer = QgsRuleBasedRenderer(root_rule)
    vlayer.setRenderer(renderer)

    # Label magnitude and region
    labeling = QgsPalLayerSettings()
    labeling.fieldName = '"magnitude" || ' | ' || "region"'
    labeling.enabled = True
    text_format = QgsTextFormat()
    text_format.setSize(9)
    labeling.setFormat(text_format)
    vlayer.setLabeling(QgsVectorLayerSimpleLabeling(labeling))
    vlayer.setLabelsEnabled(True)

    vlayer.triggerRepaint()
    print(f"✅ Loaded {vlayer.featureCount()} recent earthquake events.")
