import networkx as nx

directions = ["u", "l", "r", "d"]

def identifier(x, y, d):
    return (x, y, d)

def up_down_edge(G, x, y, d):
    G.add_edge((x, y, d), (x, y-1, d))
    G.add_edge((x, y, d), (x, y, "l"))
    G.add_edge((x, y, d), (x, y, "r"))
    G.add_edge((x, y, d), (x, y+1, d))

def right_left_edge(G, x, y, d):
    G.add_edge((x, y, d), (x-1, y, d))
    G.add_edge((x, y, d), (x, y, "u"))
    G.add_edge((x, y, d), (x, y, "d"))
    G.add_edge((x, y, d), (x+1, y, d))

def path_finding(f, t):
    x, y, d = f
    G = nx.Graph()
    for x_coor in range(x-5, x+5):
        for y_coor in range(y-5, y+5):
            up_down_edge(G, x_coor, y_coor, "u")
            up_down_edge(G, x_coor, y_coor, "d")
            right_left_edge(G, x_coor, y_coor, "l")
            right_left_edge(G, x_coor, y_coor, "r")

    return nx.shortest_path(G, f, t)

def path_finding_ignore_target_direction(f, t):
    x_to, y_to = t
    possibilities = [path_finding(f, (x_to, y_to, d)) for d in directions]
    return min(possibilities)

path_finding_ignore_target_direction((4,4,"u"), (3,2))

