import random
import time
import threading

from flask import Flask, json, request
import pyaudio
import numpy as np
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW, WHITE

app = Flask(__name__)

print("Discovering lights...")
lifx = LifxLAN(None)
devices = lifx.get_lights()
print("Found {}".format(len(devices)))


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/color/change")
def change_color():
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
    global current_mode
    current_mode = mode
    return {"mode":mode}


def light_control_loop(sleep_time=0.1):
    while True:
        for device in devices:
            if current_mode in light_modes:
                print("running light mode: {}, sleep_time {}".format(current_mode, sleep_time))
                try:
                    light_modes[current_mode](device, sleep_time=sleep_time)
                except Exception as e:
                    print("Error running light mode! error: {}".format(e))


def sparkles(bulb, sleep_time=0.05):
    zones = bulb.get_color_zones()
    zone_ids = list(range(len(zones)+1))
    for i in range(10):
        selected_zone = random.choice(zone_ids)
        for i, zone in enumerate(zones, 1):
            if i == selected_zone:
                bulb.set_zone_color(i-1,i,WHITE, 1, True)
            else:
                bulb.set_zone_color(i-1,i,[65535, 65535, 0, 65535], 1, True)
        zone_ids.remove(selected_zone)
        if len(zone_ids) == 0:
            break
        time.sleep(sleep_time)


def light_race(bulb, sleep_time=0.05):
    zones = bulb.get_color_zones()
    selected_zone = 0
    for i in range(10):
        selected_zone += 1
        for i, zone in enumerate(zones, 1):
            if i == selected_zone:
                bulb.set_zone_color(i-1,i,WHITE, 1, True)
            else:
                bulb.set_zone_color(i-1,i,[65535, 65535, 0, 65535], 1, True)
        time.sleep(sleep_time)


light_modes = {
    "sparkles": sparkles,
    "light_race": light_race
}
current_mode = "sparkles"
running_thread = None

colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
thread = threading.Thread(target=light_control_loop, args=())
thread.daemon = True
thread.start()
