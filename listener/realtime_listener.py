from __future__ import unicode_literals

from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado import gen

import logging
import json
import sys
import csv
import os

seen_unids = set()

echo_uri = 'wss://www.seismicportal.eu/standing_order/websocket'
PING_INTERVAL = 15
csv_file = "earthquakes_grassgis.csv"

# Ensure CSV file has headers (only once)
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["time", "latitude", "longitude", "magnitude", "region", "unid"])

def myprocessing(message):
    try:
        data = json.loads(message)
        props = data['data']['properties']
        coords = data['data']['geometry']['coordinates']  # [lon, lat, depth]
        lon, lat, depth = coords
        event_time = props.get('time', 'unknown')
        mag = props.get('mag', 0)
        region = props.get('flynn_region', 'unknown').replace(',', ' ').strip()
        unid = props.get('unid', 'unknown')

        if unid in seen_unids:
            return  # skip duplicate

        seen_unids.add(unid)

        with open(csv_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([event_time, lat, lon, mag, region, unid])

        logging.info(f"Saved: {event_time} | Mag: {mag} | Region: {region} | Lon: {lon}, Lat: {lat}")
    except Exception:
        logging.exception("Unable to parse json message")

@gen.coroutine
def listen(ws):
    while True:
        msg = yield ws.read_message()
        if msg is None:
            logging.info("Connection closed")
            break
        myprocessing(msg)

@gen.coroutine
def launch_client():
    try:
        logging.info("Connecting to %s", echo_uri)
        ws = yield websocket_connect(echo_uri, ping_interval=PING_INTERVAL)
    except Exception:
        logging.exception("Connection error")
    else:
        logging.info("Listening for seismic events...")
        listen(ws)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    ioloop = IOLoop.instance()
    launch_client()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        ioloop.stop()
