
from qgis.core import (
    QgsProject,
    QgsVectorLayer
)

# Load CSV as vector layer
csv_path = 'earthquakes_grassgis.csv'
uri = f'file:///{csv_path}?delimiter=,&xField=longitude&yField=latitude&crs=EPSG:4326'
layer = QgsVectorLayer(uri, 'Real-time Earthquakes', 'delimitedtext')

if not layer.isValid():
    print("⚠️ Layer failed to load.")
else:
    QgsProject.instance().addMapLayer(layer)

    # Set up HTML popup template
    html_template = """
    <html>
      <body>
        <h3 style="margin: 0;">🌍 Earthquake Info</h3>
        <b>Magnitude:</b> [% "magnitude" %]<br>
        <b>Region:</b> [% "region" %]<br>
        <b>Time:</b> [% "time" %]
      </body>
    </html>
    """

    # Apply HTML map tips (popup)
    layer.setDisplayExpression('"region"')
    layer.setMapTipTemplate(html_template)
    print("✅ HTML popup applied to earthquake layer.")
