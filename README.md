# 🌍 Real-Time Earthquake Map with QGIS + Python Automation
This project streams real-time earthquake data from the [European-Mediterranean Seismological Centre (EMSC)](https://emsc.eu/) WebSocket feed, logs it to a CSV file, and provides a complete workflow to visualize the earthquakes dynamically in **QGIS**.

This system updates every few minutes, visualizes recent seismic events, and removes events older than 48 hours.
Earthquakes are rendered as **red circles**, **scaled by magnitude**, and labeled with annotations like `5.6M`.
