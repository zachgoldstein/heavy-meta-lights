# Heavy Meta Lights

## What is this?

A light control system for heavy meta, an art car headed to burning man.

## Core goals

- Open up new ways to interact with light on the art car
- Integrate addtional inputs to control lights (audio)
- Build a better interface to control multiple strips at once

## Usage

TBD!

To start the server:
```
export FLASK_APP=src/api.py
pex flask run
```

To start the control interface:
```
pex ./light_control.py
```

## How this works (or at least is intended to)

- A bunch of lifx light strips are distributed around the art car. 
  - Each of the strips connects to a local wifi network.
- A device (like a raspi) capable of running python is connected to the same wifi network
  - This device runs a python process that uses lifx's client library to connect to and drive the light strips
  - The same device exposes some sort of simplistic interface to the local network (be it API or UI) for control over the process driving the lights

## Building

`pex` is used for easy deploys via `scp`: https://github.com/pantsbuild/pex#pex
To build the pex bundle:
....

## How can I get involved?

- Take a look at the issues list and find one of interest
- Label issue with "in-progress"
- Go for it!
- Put together a PR, flag somebody to have it merged
- Close issue

## Driving light strips
- python library to interact with lights: https://github.com/mclarkk/lifxlan


## Audio notes

pyaudio depends on portaudio, a lower level library.
To install on a mac:
```
brew install portaudio
```


<img src="https://i.imgur.com/viedxAb.gif">
