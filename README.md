# Heavy Meta Lights

## What is this?

A light control system for heavy meta, an art car headed to burning man.

## Core goals

- Open up new ways to interact with light on the art car
- Integrate addtional inputs to control lights (audio)
- Build a better interface to control multiple strips at once

## Usage

- Start the backend
```
export FLASK_APP=/home/pi/art-car/src/api.py
pipenv shell
flask run --host=0.0.0.0
```
You should see some ouput saying  "* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)"
- Navigate to the raspi ip and port 5000 on any browser on the network
  - There's a interface available at http://192.168.1.21:5000/static/test_buttons.html
- Press buttons and things
- ♪┏(・o･)┛♪┗ ( ･o･) ┓♪

## How this works (or at least is intended to)

- A bunch of lifx light strips are distributed around the art car. 
  - Each of the strips connects to a local wifi network.
- A device (like a raspi) capable of running python is connected to the same wifi network
  - This device runs a python process that uses lifx's client library to connect to and drive the light strips
  - The same device exposes some sort of simplistic interface to the local network (be it API or UI) for control over the process driving the lights

## Deploying to raspi

Note!
On a new raspberry pi you'll probably need to make sure the OS is installed and ssh is enabled

- Find the raspi IP
  - run `ping raspberrypi.local`
  - alternatively `nmap -sn 192.168.1.0/24`
- ssh into the raspi and install all dependencies (order is important):
```
ssh pi@<raspi ip>
sudo apt-get install libasound-dev portaudio19-dev python3-pyaudio python3-numpy
python3 -m pip install --user pipenv
sudo apt install libatlas3-base
pipenv lock --clear
pipenv install numpy
pipenv shell
pip install -U MarkupSafe
mkdir ./art-car
cd ./art-car
pipenv update && pipenv install
```
- Still on the raspi, add this to /etc/rc.local to make it run on startup:
```
export FLASK_APP=/home/pi/art-car/src/api.py
pipenv shell
flask run &
```
- From the host machine, copy over all files `scp -rp ./* pi@<raspi ip>:/home/pi/art-car`

## How can I get involved?

- Take a look at the issues list and find one of interest
- Label issue with "in-progress"
- Go for it!
- Put together a PR, flag somebody to have it merged
- Close issue

## Development

note, pyaudio depends on portaudio, a lower level library.
To install on a mac:
```
brew install portaudio
```

Using pipenv, setup your dev environment with all the required libs:
```
pipenv install --dev 
```

## Setting up light strips

This process really sucks. You'll need an internet connection, phone and have to install the app.
I do not have alot of confidence in this process. If light strips need to be reset often, it will be challenging without an internet connection because of the dependence on the app during this process.

If you're on android, you'll need to turn on flight mode to make sure your cellular connection does not conflict with the light strip's wifi bootstrapping process.

To setup each strip:
- Reset the strip if it's been connected previously
  - Turn it on and off 5 times
  - Press the teeny tiny button and hold for 15 seconds until the lights start to cycle
- Connect to your normal wifi
- In app, hit the "+" button (on android)
- Connect to the new network the light strip has started (starts with "LIFX")
- Add light and complete form on app

<img src="https://i.imgur.com/viedxAb.gif">
