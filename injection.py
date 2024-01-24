import json

import networkx as nx

import searcher
from zero_forcing import calculate_zero_forcing_nr


def calculate_zfr(g: nx.Graph):
    return calculate_zero_forcing_nr(
        [set(v) for v in nx.to_dict_of_lists(g).values()]) / len(g)


def inject_pendant(g: nx.Graph, i: int, j: int):
    base = len(g.nodes)
    neighbors = nx.to_dict_of_lists(g, g.nodes)
    # TODO: verify ij is an edge
    neighbors[i].remove(j)
    neighbors[j].remove(i)
    
    neighbors[base] = [i,j, base + 1]
    neighbors[base + 1] = [base, base + 2, base + 3]
    neighbors[base + 2] = [base + 1, base + 4, base + 5]
    neighbors[base + 3] = [base + 1, base + 4, base + 5]
    neighbors[base + 4] = [base + 2, base + 3, base + 5]
    neighbors[base + 5] = [base + 2, base + 3, base + 4]
    
    return nx.from_dict_of_lists(neighbors)


def inject_all(g):
    best_new_g = None
    best_ratio = calculate_zfr(g)
    for a, b in list(g.edges):
        print(f"Doing {a}-{b}")
        new_g = inject_pendant(g, a, b)
        zfr = calculate_zfr(new_g)
        if zfr > best_ratio:
            best_ratio = zfr
            best_new_g = new_g
        print(f"({a}, {b}): {zfr}")
    return best_new_g, best_ratio


g = searcher.get_graph_from_path(
    "/home/jegkocka88/temp_testing/zf_12_0.4166666666666667_c22fb9fc-738b-44ea-a1b3-a61107b29967")
print("Got the graph")

gg = inject_pendant(g, 0, 7)
print("Pendant injected")

print("Running experiment...")
ggg, zfr = inject_all(gg)

prin(f"...done, saving result (new best zfr is {zfr})")
with open("~/wow.json", 'w') as handle:
    json.dump(nx.to_dict_of_lists(ggg, ggg.nodes), handle)
print("DONE!")




