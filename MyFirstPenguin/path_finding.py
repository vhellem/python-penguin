import mynetworkx as nx

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
directions = ["top", "left", "right", "bottom"]

def up_down_edge(G, x, y, d):
    if d == "top":
        G.add_edge((x, y, d), (x, y-1, d), ACTION=ADVANCE)
        G.add_edge((x, y, d), (x, y+1, d), ACTION=RETREAT)
        G.add_edge((x, y, d), (x, y, "left"), ACTION=ROTATE_LEFT)
        G.add_edge((x, y, d), (x, y, "right"), ACTION=ROTATE_RIGHT)
    else:
        G.add_edge((x, y, d), (x, y-1, d), ACTION=RETREAT)
        G.add_edge((x, y, d), (x, y+1, d), ACTION=ADVANCE)
        G.add_edge((x, y, d), (x, y, "left"), ACTION=ROTATE_RIGHT)
        G.add_edge((x, y, d), (x, y, "right"), ACTION=ROTATE_LEFT)

def right_left_edge(G, x, y, d):
    if d == "right":
        G.add_edge((x, y, d), (x-1, y, d), ACTION=RETREAT)
        G.add_edge((x, y, d), (x+1, y, d), ACTION=ADVANCE)
        G.add_edge((x, y, d), (x, y, "top"), ACTION=ROTATE_RIGHT)
        G.add_edge((x, y, d), (x, y, "bottom"), ACTION=ROTATE_LEFT)
    else:
        G.add_edge((x, y, d), (x-1, y, d), ACTION=ADVANCE)
        G.add_edge((x, y, d), (x+1, y, d), ACTION=RETREAT)
        G.add_edge((x, y, d), (x, y, "top"), ACTION=ROTATE_LEFT)
        G.add_edge((x, y, d), (x, y, "bottom"), ACTION=ROTATE_RIGHT)

def path_finding_ignore_target_direction(f, t):
    x, y, d = f
    x_to, y_to = t
    G = nx.Graph()
    for x_coor in range(x-5, x+5):
        for y_coor in range(y-5, y+5):
            up_down_edge(G, x_coor, y_coor, "top")
            up_down_edge(G, x_coor, y_coor, "bottom")
            right_left_edge(G, x_coor, y_coor, "left")
            right_left_edge(G, x_coor, y_coor, "right")

    possibilities = [nx.shortest_path(G, f, (x_to, y_to, d)) for d in directions]
    best = min(possibilities)
    first_edge = G.get_edge_data(best[0], best[1])

    return first_edge["ACTION"]
