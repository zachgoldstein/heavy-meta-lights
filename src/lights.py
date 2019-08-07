# Drive lifx lights with interesting patterns

import asyncio
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW, WHITE
from multiprocessing import Process, Queue
import board
import busio
import adafruit_bmp280
import time


async def get_lights_periodically(light_discovery_interval=5):
    while True:
        q = Queue()
        p = Process(target=get_lights, args=(q,))
        devices = q.get()
        p.join()
        asyncio.sleep(light_discovery_interval)

def get_lights(q):
    lifx = LifxLAN(None)
    print("Discovering lights")
    discovered_lights = lifx.get_lights()
    print("Found {} devices: {}".format(len(discovered_lights), discovered_lights))
    q.put(discovered_lights)

class LightControl:
    def __init__(self, light_discovery_interval=1800, current_light_mode = "sparkles", light_control_interval = 0.0005, lta_size = 500, sta_size = 3, pressure_sensitivity = 0.1):
        self.lifx = LifxLAN(None)
        self.light_discovery_interval = light_discovery_interval
        self.light_control_interval = light_control_interval
        self.current_light_mode = current_light_mode
        self.lta_size = lta_size
        self.sta_size = sta_size
        self.pressure_sensitivity = pressure_sensitivity
        self.devices = []

        self.light_modes = {
            "sparkles": sparkles,
            "light_race": light_race
        }

    def discover_lights():
        print("Discovering lights")
        discovered_lights = lifx.get_lights()
        print("Found {} devices: {}".format(len(discovered_lights), discovered_lights))
        self.devices = discovered_lights

    async def discover_lights_continuously():
        while True:
            self.discover_lights()
            asyncio.sleep(self.light_discovery_interval)

    async def light_control_loop(devices, zone_map):
        zone_map = {}
        print("running on device...{}".format(device.mac_addr))
        if self.current_light_mode in light_modes:
            print("running light mode: {}, sleep_time {}".format(self.current_light_mode, self.light_control_interval))
            try:
                await self.light_modes[self.current_light_mode](devices, zone_map, interval=self.light_control_interval)
            except Exception as e:
                print("Error running light mode! error: {}".format(e))
        else:
            print("Mode {} not found, sleeping for five seconds".format(self.current_light_mode))
            asyncio.sleep(5)

    async def run_light_mode_continuously():
        zone_map = {}
        while True:
            if len(zone_map) > 300:
                zone_map = {}
            for device in self.devices:
                try:
                    if device.mac_addr not in zone_map:
                        zone_map[bulb.mac_addr] = device.get_color_zones()
            await light_control_loop(self.devices, zone_map)

    async def sparkles(devices, zone_map, interval=0.05):
        for device in devices:
            zones = zone_map[device.mac_addr]
            zone_ids = list(range(len(zones)+1))
            for i in range(10):
                selected_zone = random.choice(zone_ids)
                for i, zone in enumerate(zones, 1):
                    if i == selected_zone:
                        device.set_zone_color(i-1,i,WHITE, 1, True)
                    else:
                        device.set_zone_color(i-1,i,[65535, 65535, 0, 65535], 1, True)
                zone_ids.remove(selected_zone)
                if len(zone_ids) == 0:
                    break
                asyncio.sleep(interval)


    async def light_race(devices, zone_map, interval=0.05):
        for device in devices:
            zones = zone_map[device.mac_addr]
            selected_zone = 0
            for i in range(10):
                selected_zone += 1
                for i, zone in enumerate(zones, 1):
                    if i == selected_zone:
                        device.set_zone_color(i-1,i,WHITE, 1, True)
                    else:
                        device.set_zone_color(i-1,i,[65535, 65535, 0, 65535], 1, True)
                asyncio.sleep(interval)

 
    async def pressure_spike(devices, zone_map, interval = 0.0001):
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        long_light_interval = 500
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]

        current_pressure = sensor.pressure
        if self.lta_pressures is None:
            self.lta_pressures = [current_pressure]
        if self.sta_pressures is None:
            self.sta_pressures = [current_pressure]
        for i in range(10000):
            current_pressure = sensor.pressure
            self.lta_pressures.insert(0, current_pressure)
            self.sta_pressures.insert(0, current_pressure)
            if len(self.lta_pressures) > self.lta_size:
                self.lta_pressures.pop()
            if len(self.sta_pressures) > self.sta_size:
                self.sta_pressures.pop()
            lta = sum(self.lta_pressures)/len(self.lta_pressures)
            sta = sum(self.sta_pressures)/len(self.sta_pressures)
            # detection_mag = sta/lta
            detection_mag = sta - lta
            if abs(detection_mag) > self.pressure_sensitivity:
                # Trigger dragon
                print("DETECTED {}".format(detection_mag))
                color = RED
                magnitude_percent = detection_mag/self.max_pressure
                color[3] = min(65535, 65535 * magnitude_percent)
                for device in devices:
                    zones = zone_map[device.mac_addr]
                    device.set_zone_color(0,len(zones) - 1 ,color, 1, True)
            elif i%long_light_interval == 0:
                color = random.choice(colors)
                for device in devices:
                    device.set_zone_color(0,len(zones) - 1 ,color, long_light_interval, True)

            asyncio.sleep(interval)