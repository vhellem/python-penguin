from math import ceil


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
    if not can_shoot(enemy["x"], enemy["y"], body["you"]["direction"], body, youX, youY, body["you"]["weapon_range"]):
        return False

    your_weapon_power = you["weaponDamage"]
    your_strength = you["strength"]

    if not you["ammo"]:
        return False

    enemy_strength = enemy["strength"]
    enemy_weapon_range = enemy["weaponRange"]
    enemy_weapon_power = enemy["weaponPower"]
    enemy_ammo = enemy["ammo"]

    if not can_shoot(youX, youY, enemy["direction"], body, enemy["x"], enemy["y"], enemy_weapon_range):
        return True

    return will_win_shootout(your_weapon_power, enemy_weapon_power, your_strength, enemy_strength)


def will_win_shootout(your_power, enemy_power, your_strength, enemy_strength, your_turn = True):

    number_of_shoots_needed_to_kill_enemy = ceil(enemy_strength / your_power)
    number_of_shoots_needed_to_kill_you = ceil(your_strength / enemy_power)

    if your_turn:
        return number_of_shoots_needed_to_kill_enemy <= number_of_shoots_needed_to_kill_you

    return number_of_shoots_needed_to_kill_enemy < number_of_shoots_needed_to_kill_you




def enemy_in_range(enemy):
    return "x" in enemy.keys()




