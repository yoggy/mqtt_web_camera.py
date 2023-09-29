#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 si et :

import sys
import os
import datetime
import cv2
import base64
import json
import yaml
from pprint import pprint
import paho.mqtt.client as mqtt

os.chdir(os.path.dirname(__file__))

# https://qiita.com/yohm/items/e95950a5d3eba8915e99
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', buffering=1)

import logging
logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s")

with open("./config.yaml") as f:
    config = yaml.safe_load(f)

# mqtt
mqtt_client = mqtt.Client(client_id='mqtt-vosk-test', clean_session=True)
if config["mqtt_use_auth"] == True:
    mqtt_client.username_pw_set(config["mqtt_username"], config["mqtt_password"])
mqtt_client.connect(config["mqtt_host"], port=config["mqtt_port"], keepalive=60)
mqtt_client.loop_start()

# image capture from WebCamera
cap = cv2.VideoCapture(0)

for i in range(10):
  ret, img = cap.read()

cap.release()

img = cv2.resize(img, (config["jpeg_width"], config["jpeg_height"]))

ret, buf = cv2.imencode(".jpg", img, (cv2.IMWRITE_JPEG_QUALITY, config["jpeg_quality"]))

with open("img.jpg", "wb") as f:
    f.write(buf)

# publish
b64 = base64.b64encode(buf) # byte
uri = "data:image/jpeg;base64," + b64.decode()  # byte.decode() : byte->str

dt = datetime.datetime.now()
mqtt_client.publish(config["mqtt_publish_topic_time"], dt.isoformat(), retain=True)

payload = {"image":uri}
mqtt_client.publish(config["mqtt_publish_topic_img"], json.dumps(payload), retain=True)

