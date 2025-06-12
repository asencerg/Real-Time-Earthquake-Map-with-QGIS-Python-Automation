# 🌍 Real-Time Earthquake Map with QGIS + Python Automation

![Earthquake Map Demo](earthquake%20qgis.png)

This project enables a **real-time earthquake monitoring dashboard using QGIS and Python**. It streams live seismic data from the [EMSC WebSocket feed](https://www.seismicportal.eu/) and visualizes it dynamically on a world map in QGIS.  

Earthquakes appear as **circles scaled by magnitude**, **fade after 24 hours**, and are **removed after 48 hours**. Each circle is clickable, showing the **magnitude and region** in a popup.

---

## 🧠 Overview

- 📡 **Real-time CSV ingestion from EMSC**
- 🗺️ **Geospatial visualization in QGIS**
- 🕒 **Auto-expiry of events older than 48 hours**
- 📍 **Magnitude-based coloring and sizing**
- 🏷️ **Dynamic label styling**
- 🐍 **Full Python automation with PyQGIS**
- 🖥️ **Offline-compatible once CSV is downloaded**

---

## 📂 Project Structure

```
Real-Time-Earthquake-Map-with-QGIS-Python-Automation/
│
├── listener/
│   └── realtime_listener.py     # Downloads real-time earthquake data into CSV
│
├── qgis-scripts/
│   ├── realtime_loader.py       # PyQGIS: Loads and styles real-time data
│   └── realtime_popup.py        # PyQGIS: Adds interactive popups on circles
│
├── earthquakes_grassgis.csv     # Output CSV with recent earthquake data
├── earthquake qgis.png          # Screenshot of QGIS map
├── LICENSE
└── README.md                    # You are here!
```

---

## ⚙️ 1. Earthquake Data Listener

This script listens to real-time seismic data and writes it to a CSV:

### ▶ `listener/realtime_listener.py`

```bash
python listener/realtime_listener.py
```

✅ This script:

- Connects to EMSC's real-time WebSocket feed.
- Parses each earthquake event.
- Writes events to `earthquakes_grassgis.csv`.
- Avoids duplicates using event IDs (`unid`).
- Appends new rows continuously.

The output CSV includes:

```csv
time,latitude,longitude,magnitude,region,unid
2025-06-11T23:55:10Z,38.29,27.12,5.6,"Aegean Sea",us7000jklm
```

---

## 🗺️ 2. Load and Visualize in QGIS

Use the PyQGIS script inside QGIS Python Console or create a scheduled task with `qgis --code`.

### ▶ `qgis-scripts/realtime_loader.py`

```bash
# Inside QGIS Python Console:
exec(open('qgis-scripts/realtime_loader.py').read())
```

✅ This script:

- Loads `earthquakes_grassgis.csv` as a point layer.
- Styles circles **proportional to magnitude** (from small green to large red).
- Fades earthquakes **after 24 hours**.
- Removes earthquakes **older than 48 hours**.
- Labels events with `"Mag: 6.2"` on the map.
- Scales properly as you zoom in.

### Magnitude Styling:
| Magnitude | Color       | Circle Size |
|-----------|-------------|-------------|
| < 2.5     | 🟢 Light Green | Small        |
| 2.5–4.5   | 🟡 Yellow      | Medium       |
| 4.5–6.0   | 🟠 Orange      | Large        |
| > 6.0     | 🔴 Red         | Extra Large  |

---

## 💬 3. Interactive Popups

### ▶ `qgis-scripts/realtime_popup.py`

```bash
# Inside QGIS Python Console:
exec(open('qgis-scripts/realtime_popup.py').read())
```

✅ This script adds:

- **Click-to-view** popup with `Magnitude` and `Region`
- Fully interactive info balloons
- Works with QGIS built-in Identify Tool

---

## 🔁 Automate Everything

You can automate the real-time pipeline by running:

1. The listener script continuously:
```bash
python listener/realtime_listener.py
```

2. The QGIS PyQGIS loader on a loop:
```bash
qgis --code qgis-scripts/realtime_loader.py
```

(Use Task Scheduler, cron, or a loop script every few minutes.)

---

## 📌 Requirements

- QGIS 3.28+ installed
- Python 3.8+ (comes with QGIS)
- WebSocket-compatible internet connection
- Compatible with Windows, macOS, Linux

---

## 📤 Export to Web

You can export this map to the web using:

- `qgis2web` plugin (Leaflet or OpenLayers)
- `Lizmap` for live publishing
- Export to GeoPackage + host via MapLibre

---

## 📜 License

[MIT License](LICENSE)

---

## 🌐 Credits

- [EMSC-CSEM](https://www.emsc-csem.org/)
- [QGIS](https://qgis.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)


---

> **Built with QGIS + Python to bring seismic intelligence to your desktop in real-time.**
