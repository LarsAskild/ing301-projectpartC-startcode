# Install FastAPI framework
# pip3 install "fastapi[all]"
# https://fastapi.tiangolo.com/tutorial/

# uvicorn main:app --reload

import uvicorn

from fastapi import FastAPI, Response, status
from fastapi.staticfiles import StaticFiles
from typing import Union

from demohouse import build_demo_house
from device import Device
from sensors import *
from actuators import *


app = FastAPI()

smart_house = build_demo_house()

# http://localhost:8000/welcome/index.html
app.mount("/welcome", StaticFiles(directory="static"), name="static")


# http://localhost:8000/
@app.get("/")
def root():
    return {"message": "Welcome to SmartHouse Cloud REST API - Powered by FastAPI"}


@app.get("/smarthouse/")
def read_smarthouse():
    return smart_house


@app.get("/smarthouse/floor/")
def read_floors():
    return smart_house.floors


@app.get("/smarthouse/floor/{fid}")
def read_floor(fid: int, response: Response):
    return smart_house.floors[fid]


@app.get("/smarthouse/floor/{fid}/room")
def read_rooms(fid: int, response: Response):
    return smart_house.floors[fid].rooms


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def read_room(fid: int, rid: int, response: Response):
    return smart_house.floors[fid].rooms[rid]


@app.get("/smarthouse/device")
def read_devices():
    device = []
    for floor in smart_house.floors:
        for room in floor.rooms:
            for device_ in room.devices:
                device.append(device_)            
    return device


@app.get("/smarthouse/device/{did}")
def read_room(did: int, response: Response):
    device = []
    for floor in smart_house.floors:
        for room in floor.rooms:
            for device_ in room.devices:
                if(device_.did == did):
                    device = device_
    return device




if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
