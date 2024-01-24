import json
import logging
import os
import random
import typing
import uuid
import sys
from collections import deque

import click
import networkx as nx
from tqdm import tqdm

from zero_forcing import calculate_zero_forcing_nr


logger = logging.getLogger(__name__)



def get_full_paths_for_graph_size(result_dir: str, size: int) -> typing.List[str]:
    paths = [os.path.join(result_dir, f) for f in os.listdir(result_dir)
            if f'zf_{size}' in f]
    logger.info(f"Loaded {len(paths)} paths with size {size} from {result_dir}")
    return paths


def get_neighbors_from_path(path: str) -> typing.Dict[int, typing.List[int]]:
    with open(path, 'r') as handle:
        neighbors = json.load(handle)
        return {int(k): set(v) for k, v in neighbors.items()}


def get_graph_from_neighbors(neighbors: typing.Dict[int, typing.List[int]]) -> nx.Graph:
    return nx.from_dict_of_lists(neighbors)


def get_graph_from_path(path):
    return get_graph_from_neighbors(get_neighbors_from_path(path))


def is_connected(neighbors: typing.Dict[int, typing.List[int]]) -> bool:
    have_seen = {0}
    todo = deque([0])
    while todo:
        act = todo.popleft()
        for neighbor in neighbors[act]:
            if neighbor not in have_seen:
                have_seen.add(neighbor)
                todo.append(neighbor)
    return len(have_seen) == len(neighbors)


def is_new_graph(graphs: typing.List[nx.Graph], candidate: nx.Graph) -> bool:
    for graph in graphs:
        if nx.is_isomorphic(graph, candidate):
            return False
    return True


def search(n: int, d: int, iterations: int):
    """
    Performs zero-forcing simulation on <iterations> many randomly chosen d-regular graphs on n vertices.
    Returns the Graph G, the neighborhood list, and the zero-forcing ratio of the graph
    with the highest zero-forcing number.
    """
    best_zfr = 0
    best_neighbors = None
    best_G = None
    for i in tqdm(range(iterations)):
        G = nx.random_regular_graph(d, n)
        all_neighbors = {
            x: {int(y) for y in G.neighbors(x)} for x in sorted(list(G.nodes))
        }
        if is_connected(all_neighbors):
            zfn = calculate_zero_forcing_nr(all_neighbors)
            zfr = zfn / n
            if zfr > best_zfr:
                best_zfr = zfr
                best_neighbors = all_neighbors
                best_G = G
    return (best_G, best_neighbors, best_zfr)


def save_result(neighbors, ratio, result_dir):
    logger.debug(f"Reporting ratio: {ratio}")
    filename = f"zf_{len(neighbors)}_{ratio}_{uuid.uuid4()}"
    filepath = os.path.join(result_dir, filename)

    logger.debug(f" Writing result to {filepath}")
    jsonified_neighbors = {k: list(v) for k, v in neighbors.items()}
    with open(filepath, 'w') as handle:
        json.dump(jsonified_neighbors, handle)


@click.command()
@click.option("-a", "--graph_size_min", type=int, help="Minimum size of the graphs")
@click.option("-z", "--graph_size_max", type=int, help="Maximum size of the graphs")
@click.option("-r", "--rounds", type=int, default=None, help="Number of rounds to perform (default is infinite)")
@click.option("-i", "--iterations", type=int, help="Number of iterations")
@click.option("-p", "result_dir", type=str, help="Path to result folder")
@click.option("-l", "--loglevel", default="WARNING", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False))

def main(graph_size_min, graph_size_max, rounds, iterations, result_dir, loglevel):
    logging.basicConfig(stream=sys.stdout, level=logging.__dict__.get(loglevel))
    round_cnt = 0
    while not rounds or round_cnt < rounds:
        logger.info(f"Running round #{round_cnt + 1}")
        graph_size = random.choice(list(range(graph_size_min // 2 * 2 , graph_size_max + 2, 2)))
        existing_graph_paths = get_full_paths_for_graph_size(result_dir, graph_size)
        existing_graphs = [get_graph_from_neighbors(get_neighbors_from_path(path))
                           for path in existing_graph_paths]
        logger.debug(f"checking graph size {graph_size}")
        g, neighbors, zfr = search(graph_size, 3, iterations)
        if is_new_graph(existing_graphs, g):
            logger.debug(f"New graph found with zfr {zfr}")
            existing_graphs.append(g)
            save_result(neighbors, zfr, result_dir)
        else:
            logger.debug(f"Duplicate found with zfr {zfr}")
        logger.debug('Cycle finished.')
        round_cnt += 1


if __name__ == "__main__":
    main()
