import networkx as nx
import sys

from collections import deque
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

def report(neighbors, ratio):
    filename = f"zf_{len(neighbors)}_{ratio}"
    with open(filename, 'w') as FILE:
        FILE.write(f"Ratio is {ratio}\n")
        for neighbor in neighbors:
            FILE.write(str(neighbor) + "\n")

def search():
    n = int(sys.argv[1])
    d = int(sys.argv[2])
    iterations = int(sys.argv[3])
    best_zfr = 0
    best_neighbors = None
    for i in tqdm(range(iterations)):
        G = nx.random_regular_graph(d,n)
        all_neighbors = [set(G.neighbors(x)) for x in G.nodes]
        if is_connected(all_neighbors):
            zfn = calculate_zero_forcing_nr(all_neighbors)
            zfr = zfn / n
            if zfr > best_zfr:
                best_zfr = zfr
                best_neighbors = all_neighbors
    report(best_neighbors, best_zfr)

if __name__ == "__main__":
    search()
