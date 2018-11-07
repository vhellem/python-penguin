from math import ceil
import random
from path_finding import path_finding_ignore_target_direction

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

ROTATE_UP =  {"top" : PASS, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
ROTATE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : PASS, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
GET_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : PASS ,"left" : ROTATE_LEFT }
GET_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : PASS }

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

def can_shoot(x, y, currentDir, body, youX, youY, weapon_range):

    if x!=youX and y!=youY:
        return False

    if x == youX:
        if abs(y-youY) > weapon_range:
            return False
        if youY > y and currentDir == "top":
            for wall in body["walls"]:
                if wall["x"]==x and wall["y"]>y and wall["y"]<youY:
                        return False
            return True
        if youY < y and currentDir == "bottom":
            for wall in body["walls"]:
                if wall["x"]==x and wall["y"]>youY and wall["y"]<y:
                        return False
            return True
        return False
    else:
        if abs(x-youX) > weapon_range:
            return False
        if youX > x and currentDir == "left":
            for wall in body["walls"]:
                if wall["y"]==y and wall["x"]>x and wall["x"]<youX:
                        return False
            return True
        if youX < x and currentDir == "right":
            for wall in body["walls"]:
                if wall["y"]==y and wall["x"]<x and wall["x"]> youX:
                        return False
            return True
        return False

def should_shoot_enemy(body):

    """
    Calculates whether you should shoot the enemy,
    does not take into advantage whether the enemy can turn, will win a shootout and you cannot run
    :param body:
    :return:
    """
    enemy = body["enemies"][0]
    if not enemy:
        return False

    you = body["you"]
    youX = you["x"]
    youY = you["y"]
    if not can_shoot(enemy["x"], enemy["y"], body["you"]["direction"], body, youX, youY, body["you"]["weaponRange"]):
        return False

    your_weapon_power = you["weaponDamage"]
    your_strength = you["strength"]

    if not you["ammo"]:
        return False

    enemy_strength = enemy["strength"]
    enemy_weapon_range = enemy["weaponRange"]
    enemy_weapon_power = enemy["weaponDamage"]
    enemy_ammo = enemy["ammo"]

    if not can_shoot(youX, youY, enemy["direction"], body, enemy["x"], enemy["y"], enemy_weapon_range):
        return True

    return will_win_shootout(your_weapon_power, enemy_weapon_power, your_strength, enemy_strength)


def will_win_shootout(your_power, enemy_power, your_strength, enemy_strength, your_turn = 0):

    number_of_shoots_needed_to_kill_enemy = ceil(enemy_strength / your_power)
    number_of_shoots_needed_to_kill_you = ceil(your_strength / enemy_power)

    return number_of_shoots_needed_to_kill_enemy <= number_of_shoots_needed_to_kill_you-your_turn



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


def enemy_in_range(enemy):
    return "x" in enemy.keys()



def should_flee(body):
    you = body["you"]
    enemy = body["enemies"][0]

    if can_shoot(you["x"], you["y"], enemy["direction"], body, enemy["x"], enemy["y"], enemy["weaponRange"]):
        your_turn = 1
        if enemy["direction"] == you["direction"]:
            your_turn = 2

        return not will_win_shootout(you["weaponDamage"], enemy["weaponDamage"], you["strength"], enemy["strength"], your_turn)

    return False


def choose_penguin_action(body):
    if in_fire(body):
        return escape_from_fire(body)

    if enemy_in_range(body["enemies"][0]):
        if should_shoot_enemy(body):
            return "shoot"
        if should_flee(body):
            return where_to_flee(body)


        return how_to_engage(body)
    if bonus_in_range(body):
        return move_towards(select_best_bonus(body), body)
    return random_move_without_wall(body)

def random_move_without_wall(body):
    choices = ["rotate-left", "rotate-right", "advance"]
    #TODO: Do not rotate towards a wall
    youX = body["you"]["x"]
    youY = body["you"]["y"]
    d = body["you"]["direction"]
    x, y = body["maxWidth"]//2, body["maxHeight"]//2

    if abs(youX-x) + abs(youY-y) <= 3:
        action = ADVANCE
        if wallInFrontOfPenguin(body):
            return random.choice[ROTATE_LEFT, ROTATE_RIGHT]
        return action

    action, _ = path_finding_ignore_target_direction((youX, youY, d), (x, y), create_not_allowed(body))

    if random.random() > 0.7:
        return SHOOT
    if not action:
        action = ADVANCE
        if wallInFrontOfPenguin(body):
            return random.choice[ROTATE_LEFT, ROTATE_RIGHT]
        return action

    return action

def add_map_border_to_set(body, not_allowed):
    mapH = body["mapHeight"]
    mapW = body["mapWidth"]
    for i in range(-1, mapH + 1):
        not_allowed.add((-1, i))
        not_allowed.add((mapW + 1, i))
    for i in range(-1, mapW + 1):
        not_allowed.add((i, -1))
        not_allowed.add((i, mapH + 1))

def create_not_allowed(body):
    not_allowed = set()
    add_map_border_to_set(body, not_allowed)
    for w in body["walls"]:
        not_allowed.add((w["x"], w["y"]))
    for f in body["fire"]:
        not_allowed.add((f["x"], f["y"]))
    #for e in body["enemies"]:
        #if "x" in e.keys():
            #not_allowed.add((e["x"], e["y"]))

    return not_allowed

def move_towards(tuple, body):
    if tuple is None:
        #TODO
        return "move_towards None"
    x, y = tuple
    you = body["you"]
    youX = you["x"]
    youY = you["y"]
    d = you["direction"]
    action, _ = path_finding_ignore_target_direction((youX,youY,d), (x,y), create_not_allowed(body))
    return action

def select_best_bonus(body):
    my_x = body["you"]["x"]
    my_y = body["you"]["y"]
    my_d = body["you"]["direction"]
    min_l = 100000
    best = None
    for bonus in body["bonusTiles"]:
        x, y = bonus["x"], bonus["y"]
        l = abs(x-my_x) + abs(y-my_y)
        if l < min_l:
            best = (x, y)
            min_l = l

    return best

def bonus_in_range(body):
    return len(body["bonusTiles"])>0

def is_enemy_advance_unobstructed(body):
    you = body["you"]
    enemy = body["enemies"][0]

    if you["x"] > enemy["x"]:
        if you["y"] > enemy["y"]:
            if can_shoot(enemy["x"], enemy["y"]+1, "left", body, you["x"], you["y"], you["weaponRange"]):
                return True
            if can_shoot(enemy["x"]+1, enemy["y"], "top", body, you["x"], you["y"], you["weaponRange"]):
                return True

        else:
            if can_shoot(enemy["x"], enemy["y"]-1, "left", body, you["x"], you["y"], you["weaponRange"]):
                return True
            if can_shoot(enemy["x"]+1, enemy["y"], "bottom", body, you["x"], you["y"], you["weaponRange"]):
                return True
    else:
        if you["y"] > enemy["y"]:
            if can_shoot(enemy["x"], enemy["y"]+ 1, "right", body, you["x"], you["y"], you["weaponRange"]):
                return True
            if can_shoot(enemy["x"] - 1, enemy["y"], "top", body, you["x"], you["y"], you["weaponRange"]):
                return True
        else:
            if can_shoot(enemy["x"], enemy["y"] - 1, "right", body, you["x"], you["y"], you["weaponRange"]):
                return True
            if can_shoot(enemy["x"] - 1, enemy["y"], "bottom", body, you["x"], you["y"], you["weaponRange"]):
                return True
    return False


def how_to_engage(body):
    you = body["you"]
    enemy = body["enemies"][0]
    if not will_win_shootout(you["weaponDamage"], enemy["weaponDamage"], you["strength"], enemy["strength"]):
        return where_to_flee(body)
    if not will_win_shootout(you["weaponDamage"], enemy["weaponDamage"], you["strength"], enemy["strength"], 1):
        if enemy_is_far_away(body):
            if bonus_in_range(body):
                return move_towards(select_best_bonus(body), body)
        elif is_enemy_advance_unobstructed(body):
            return rotate_towards_enemy(body)
    return move_towards_enemy(body)

def enemy_is_far_away(body):
    you = body["you"]
    enemy = body["enemies"][0]

    if abs(you["x"]-enemy["x"])>=2 and abs(you["y"]-enemy["y"])>=2:
        return True

    return False

def move_towards_enemy(body):
    enemy = body["enemies"][0]
    return move_towards((enemy["x"], enemy["y"]), body)



def rotate_towards_enemy(body):
    you = body["you"]
    enemy = body["enemies"][0]

    if you["x"] > enemy["x"]:
        if you["y"] > enemy["y"]:
            possibleMoves = (GET_LEFT[you["direction"]], ROTATE_UP[you["direction"]])
            if enemy["direction"] == "bottom" or enemy["direction"] == "top":
                return possibleMoves[0]
            return possibleMoves[1]
        else:
            possibleMoves = (GET_LEFT[you["direction"]], ROTATE_DOWN[you["direction"]])
            if enemy["direction"] == "top" or enemy["direction"] == "bottom":
                return possibleMoves[0]
            return possibleMoves[1]
    else:
        if you["y"] > enemy["y"]:
            possibleMoves = (GET_RIGHT[you["direction"]], ROTATE_UP[you["direction"]])
            if enemy["direction"] == "bottom" or enemy["direction"] == "top":
                return possibleMoves[0]
            return possibleMoves[1]
        else:
            possibleMoves = (GET_RIGHT[you["direction"]], ROTATE_DOWN[you["direction"]])
            if enemy["direction"] == "top" or enemy["direction"] == "bottom":
                return possibleMoves[0]
            return possibleMoves[1]



def where_to_flee(body):
    action = RETREAT
    you = body["you"]
    enemy = body["enemies"][0]
    if wallBehindPenguin(body) or (you["direction"] == enemy["direction"] and can_shoot(you["x"], you["y"], enemy["direction"], body, enemy["x"], enemy["y"], enemy["weaponRange"])):
        action = random.choice([ROTATE_LEFT, ROTATE_RIGHT])


    return action





def in_fire(body):
    you = body["you"]

    for fire in body["fire"]:
        if fire["x"]==you["x"] and fire["y"]==you["y"]:
            return True
    return False

def escape_from_fire(body):
    return where_to_flee(body)


def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]
    mapwidth = body["mapWidth"]
    mapheight = body["mapHeight"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall, mapwidth, mapheight)

def wallBehindPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]
    mapwidth = body["mapWidth"]
    mapheight = body["mapHeight"]

    if bodyDirection == "top":
        yValueToCheckForWall += 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall -= 1
    elif bodyDirection == "left":
        xValueToCheckForWall += 1
    elif bodyDirection == "right":
        xValueToCheckForWall -= 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall, mapwidth, mapheight)

def doesCellContainWall(walls, x, y, mapwidth, mapheight):
    if x<0 or y<0 or x >= mapwidth or y>= mapheight:
        return True
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False


def main():
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
    "direction": "right",
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
        "x": 29,
        "y": 4,
      "direction": "left",
      "strength": 300,
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
    print(choose_penguin_action(body))
