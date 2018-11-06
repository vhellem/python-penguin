ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
directions = ["top", "left", "right", "bottom"]

def get_path(q, parent):
    last_parent = q
    while parent.get(q, None):
        last_parent = q
        q = parent[q]
    return last_parent

def neighbours(q, not_allowed):
    for n in all_neighbours(q):
        if not (n[0], n[1]) in not_allowed:
            yield n

def all_neighbours(q):
    x, y, d = q
    if d == "top":
        yield (x, y-1, d)
        yield (x, y+1, d)
        yield (x, y, "left")
        yield (x, y, "right")
    elif d == "bottom":
        yield (x, y-1, d)
        yield (x, y+1, d)
        yield (x, y, "left")
        yield (x, y, "right")
    elif d == "right":
        yield (x-1, y, d)
        yield (x+1, y, d)
        yield (x, y, "top")
        yield (x, y, "bottom")
    elif d == "left":
        yield (x-1, y, d)
        yield (x+1, y, d)
        yield (x, y, "top")
        yield (x, y, "bottom")

def path_finding_ignore_target_direction(f, t, not_allowed):
    x, y, d = f
    x_to, y_to = t

    parent = {}
    visited = {}
    frontier = [(x, y, d)]
    while len(frontier) > 0:
        q = frontier.pop(0)
        if (q[0], q[1]) == (x_to, y_to):
            return get_path(q, parent)
        visited[q] = True
        for n in neighbours(q, not_allowed):
            if not visited.get(n, False):
                parent[n] = q
                frontier.append(n)
    return None

f_node = (1,0,"top")
t_node = (1,2)

while (f_node[0], f_node[1]) != t_node:
    print(f_node)
    f_node = path_finding_ignore_target_direction(f_node, t_node, [(0,1),(1,1),(2,1)]) 
