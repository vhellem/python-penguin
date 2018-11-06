import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'venv/Lib/site-packages')))

import json
import time
import random
import math
from utils import choose_penguin_action

#from path_finding import path_finding_ignore_target_direction

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)

def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction =  MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
    return plannedAction

def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

def action_from_tile_to_tile(f, t):
    x, y, d = f
    x_to, y_to, d_to = t


def chooseAction(body):
    you = body["you"]
    x = you["x"]
    y = you["y"]
    d = you["direction"]
    #action = path_finding_ignore_target_direction((x,y,d), (2,2)) #choose_penguin_action(body)
    action = choose_penguin_action(body)
    return action

body = {
  "matchId": "d191f1cc-c179-4779-b649-af5e9dab198e",
  "mapWidth": 20,
  "mapHeight": 20,
  "wallDamage": 30,
  "penguinDamage": 50,
  "weaponDamage": 60,
  "visibility": 5,
  "weaponRange": 5,
  "you": {
    "direction": "top",
    "x": 29,
    "y": 8,
    "strength": 300,
    "ammo": 995,
    "status": "firing",
    "targetRange": 4,
    "weaponRange": 5,
    "weaponDamage": 60
  },
  "enemies": [
    {
      "direction": "bottom",
      "strength": 240,
      "ammo": 1000,
      "status": "hit",
      "weaponRange": 5,
      "weaponDamage": 60
    }
  ],
  "walls": [
    {
      "x": 16,
      "y": 7,
      "strength": 200
    },
    {
      "x": 18,
      "y": 7,
      "strength": 200
    },
    {
      "x": 17,
      "y": 7,
      "strength": 200
    },
    {
      "x": 15,
      "y": 7,
      "strength": 200
    }
  ],
  "bonusTiles": [
   {
      "x": 12,
      "y": 5,
      "type": "weapon-range",
      "value": 1
  },
  {
      "x": 15,
      "y": 11,
      "type": "strength",
      "value": 3
  },
  {
      "x": 17,
      "y": 10,
      "type": "weapon-damage",
      "value": 4
  }],
  "suddenDeath": 10,
  "fire": []
}

print(chooseAction(body))

env = os.environ
req_params_query = "command" #env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}


if req_params_query == "info":
    returnObject["name"] = "Pingu"
    returnObject["team"] = "Team Python"
elif req_params_query == "command":
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()
