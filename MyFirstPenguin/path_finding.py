ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
directions = ["top", "left", "right", "bottom"]

def get_path(q, parent):
    path_length = 1
    last_parent = q
    while parent.get(q, None):
        path_length += 1
        last_parent = q
        q = parent[q]
    return (last_parent, path_length)

def neighbours(q, not_allowed):
    for n, a in all_neighbours(q):
        if not (n[0], n[1]) in not_allowed:
            yield (n, a)

def all_neighbours(q):
    x, y, d = q
    if d == "top":
        yield ((x, y-1, d), ADVANCE)
        yield ((x, y+1, d), RETREAT)
        yield ((x, y, "left"), ROTATE_LEFT)
        yield ((x, y, "right"), ROTATE_RIGHT)
    elif d == "bottom":
        yield ((x, y-1, d), RETREAT)
        yield ((x, y+1, d), ADVANCE)
        yield ((x, y, "left"), ROTATE_RIGHT)
        yield ((x, y, "right"), ROTATE_LEFT)
    elif d == "right":
        yield ((x-1, y, d), RETREAT)
        yield ((x+1, y, d), ADVANCE)
        yield ((x, y, "top"), ROTATE_LEFT)
        yield ((x, y, "bottom"), ROTATE_RIGHT)
    elif d == "left":
        yield ((x-1, y, d), ADVANCE)
        yield ((x+1, y, d), RETREAT)
        yield ((x, y, "top"), ROTATE_RIGHT)
        yield ((x, y, "bottom"), ROTATE_LEFT)

def path_finding_ignore_target_direction(f, t, not_allowed):
    print("PATH")
    x, y, d = f
    x_to, y_to = t

    action = {}
    parent = {}
    visited = {}
    frontier = [(x, y, d)]
    while len(frontier) > 0:
        q = frontier.pop(0)
        if (q[0], q[1]) == (x_to, y_to):
            next_tile, path_len = get_path(q, parent)
            print("PATH2")
            return action[next_tile], path_len
        visited[q] = True
        for n, a in neighbours(q, not_allowed):
            if not visited.get(n, False):
                parent[n] = q
                action[n] = a
                frontier.append(n)
    return None
