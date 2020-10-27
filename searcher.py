import networkx as nx
import os
import re
import sys

from collections import deque
from datetime import datetime
from tqdm import tqdm
from zero_forcing import calculate_zero_forcing_nr


def is_connected(neighbors):
    have_seen = {0}
    todo = deque([0])
    while todo:
        act = todo.popleft()
        for neighbor in neighbors[act]:
            if neighbor not in have_seen:
                have_seen.add(neighbor)
                todo.append(neighbor)
    return len(have_seen) == len(neighbors)


def get_full_paths_for_graph_size(result_dir, size):
    paths = [os.path.join(result_dir, f) for f in os.listdir(result_dir)
            if f'zf_{size}' in f]
    print(f"Loaded {len(paths)} paths with size {size} from {result_dir}")
    return paths


def get_neighbors_from_path(path):
    regex = '{(\d+), (\d+), (\d+)}'
    with open(path, 'r') as HANDLER:
        content = HANDLER.read()
        return re.findall(regex, content)


def get_graph_from_neighbors(neighbors):
    G = nx.Graph()
    G.add_nodes_from(range(len(neighbors)))
    for i, n_set in enumerate(neighbors):
        for j in n_set:
            if int(i) < int(j):
                G.add_edge(int(i),int(j))
    return G


def is_new_graph(graphs, candidate):
    for graph in graphs:
        if nx.is_isomorphic(graph, candidate):
            return False
    return True


def search(n, d, iterations):
    best_zfr = 0
    best_neighbors = None
    best_G = None
    for i in tqdm(range(iterations)):
        G = nx.random_regular_graph(d,n)
        all_neighbors = [set(G.neighbors(x)) for x in sorted(list(G.nodes))]
        if is_connected(all_neighbors):
            zfn = calculate_zero_forcing_nr(all_neighbors)
            zfr = zfn / n
            if zfr > best_zfr:
                best_zfr = zfr
                best_neighbors = all_neighbors
                best_G = G
    return (G, best_neighbors, best_zfr)


def report(neighbors, ratio, result_dir):
    print(f"Reporting ratio: {ratio}")
    timestamp_str = datetime.now().strftime("%d_%m_%y_%H:%M_%S")
    filename = f"zf_{len(neighbors)}_{ratio}_{timestamp_str}"
    filepath = os.path.join(result_dir, filename)
    print(f"Reporting result to {filepath}")
    with open(filepath, 'w') as FILE:
        FILE.write(f"Ratio is {ratio}\n")
        for neighbor in neighbors:
            FILE.write(str(neighbor) + "\n")

if __name__ == "__main__":
    result_dir = "/home/jegkocka88/forcing_results"
    n = int(sys.argv[1])
    iterations = int(sys.argv[2])
    existing_graph_paths = get_full_paths_for_graph_size(result_dir, n)
    existing_graphs = [get_graph_from_neighbors(get_neighbors_from_path(path))
                       for path in existing_graph_paths]
    while True:
        print(f"checking graph size {n}")
        g, neighbors, zfr = search(n, 3, iterations)
        if is_new_graph(existing_graphs, g):
            print(f"New graph found with zfr {zfr}")
            existing_graphs.append(g)
            report(neighbors, zfr, result_dir)
        else:
            print(f"Duplicate found with zfr {zfr}")
        print('Cycle finished.')
