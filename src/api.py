import random
import time
import datetime
import threading

from flask import Flask, json, request
import numpy as np
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW, WHITE

from lights import LightControl

app = Flask(__name__)

light_control = LightControl()

app_state = {
    "sensitivity": 0.1,
    "light_command_frequency": 0.0005,
    "sensor_poll_frequency": 0.00001,
}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/color/change")
def change_color():
    global light_control
    light_control.current_light_mode = None
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    color = random.choice(colors)
    print("Attempting to change color to {}".format(color))
    for device in devices:
        device.set_color(color, 10, True)
    return {"color":color}


@app.route("/mode", methods=['POST'])
def post_mode():
    json_data = request.get_json()
    if 'mode' not in json_data:
        return {}
    mode = json_data['mode']
    print("Setting light control mode to {}".format(mode))
    global light_control
    light_control.current_light_mode = mode
    return {"mode":mode}


@app.route("/stats", methods=['GET'])
def get_app_stats():
    json_data = request.get_json()
    if 'mode' not in json_data:
        return {}
    mode = json_data['mode']
    print("Setting light control mode to {}".format(mode))
    global current_mode
    current_mode = mode
    return {"mode":mode}


asyncio.run(light_control.discover_lights_continuously())
asyncio.run(light_control.run_light_mode_continuously())