import random

from flask import Flask
import pyaudio
import numpy as np
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW

app = Flask(__name__)

print("Discovering lights...")
lifx = LifxLAN(None)
devices = lifx.get_lights()

print("Found {}".format(len(devices)))

colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/color/change")
def change_color():
    color = random.choice(colors)
    print("Attempting to change color to {}".format(color))
    # bulb = devices[0]
    # bulb.set_color(color, 10, True)
    return {"color":color}
