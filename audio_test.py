# Experiment to drive lifxlan strip with audio levels

import pyaudio
import numpy as np
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)


print("Discovering lights...")
lifx = LifxLAN(None)
devices = lifx.get_lights()
bulb = devices[0]

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
for i in range(int(10*44100/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    num_bars = int(50*peak/2**16)
    bars="#"*num_bars
    color = colors[num_bars%len(colors)]
    bulb.set_color(color, i, True)
    print("%04d %05d %s"%(i,peak,bars))

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()
