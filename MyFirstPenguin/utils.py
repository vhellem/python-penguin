from math import ceil
import random

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

ROTATE_UP =  {"top" : PASS, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
ROTATE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : PASS, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
ROTATE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : PASS ,"left" : ROTATE_LEFT }
ROTATE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : PASS }

def can_shoot(x, y, currentDir, body, youX, youY, weapon_range):

    if x!=youX and y!=youY:
        return False

    if x == youX:
        if abs(y-youY) > weapon_range:
            return False
        if youY > y and currentDir == "bottom":
            for wall in body["walls"]:
                if wall["x"]==x and wall["y"]>y and wall["y"]<youY:
                        return False
            return True
        if youY < y and currentDir == "top":
            for wall in body["walls"]:
                if wall["x"]==x and wall["y"]>youY and wall["y"]<y:
                        return False
            return True
        return False
    else:
        if abs(x-youX) > weapon_range:
            return False
        if youX > x and currentDir == "right":
            for wall in body["walls"]:
                if wall["y"]==y and wall["x"]>x and wall["x"]<youX:
                        return False
            return True
        if youX < x and currentDir == "left":
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

    while True:
        choice = random.choice(choices)
        if choice == "advance" and wallInFrontOfPenguin(body):
            continue
        return choice

def move_towards(tuple, body):
    x, y = tuple
    return "advance"

def select_best_bonus(body):
    return body["bonusTiles"][0]["x"], body["bonusTiles"][0]["y"]

def bonus_in_range(body):
    return len(body["bonusTiles"])>0



def how_to_engage(body):
    you = body["you"]
    enemy = body["enemies"][0]
    if not will_win_shootout(you["weaponDamage"], enemy["weaponDamage"], you["strength"], enemy["strength"]):
        return where_to_flee(body)
    if not will_win_shootout(you["weaponDamage"], enemy["weaponDamage"], you["strength"], enemy["strength"], 1):
        return rotate_towards_enemy(body)
    return move_towards_enemy(body)

def move_towards_enemy(body):
    return ADVANCE



def rotate_towards_enemy(body):
    you = body["you"]
    enemy = body["enemies"][0]

    if you["x"] > enemy["x"]:
        if you["y"] > enemy["y"]:
            possibleMoves = (ROTATE_LEFT[you["direction"]], ROTATE_UP["direction"])
            if enemy["direction"] == "down":
                return possibleMoves[0]
            return possibleMoves[1]
        else:
            possibleMoves = (ROTATE_LEFT[you["direction"]], ROTATE_DOWN["direction"])
            if enemy["direction"] == "up":
                return possibleMoves[0]
            return possibleMoves[1]
    else:
        if you["y"] > enemy["y"]:
            possibleMoves = (ROTATE_RIGHT[you["direction"]], ROTATE_UP["direction"])
            if enemy["direction"] == "down":
                return possibleMoves[0]
            return possibleMoves[1]
        else:
            possibleMoves = (ROTATE_RIGHT[you["direction"]], ROTATE_DOWN["direction"])
            if enemy["direction"] == "up":
                return possibleMoves[0]
            return possibleMoves[1]



def where_to_flee(body):
    return "advance"

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
    print(choose_penguin_action(body))


