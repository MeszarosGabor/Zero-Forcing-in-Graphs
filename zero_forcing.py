import logging
import typing
from itertools import combinations

logger = logging.getLogger(__name__)


class ZeroForcing:
    def __init__(self, neighbors: typing.Dict[int, typing.Set[int]], forcing_set: typing.Set[int]):
        self.n = len(neighbors)
        self.neighbors = neighbors
        self.forcing_set = forcing_set
        self.black_neighbor_counter = [0 for x in range(0, self.n)]
        self.passive_black = set()

        for node in self.forcing_set:
            for neighbor in self.neighbors[node]:
                self.black_neighbor_counter[neighbor] += 1
        for node in self.forcing_set:
            if self.black_neighbor_counter[node] == len(self.neighbors[node]):
                self.passive_black.add(node)
        self.active_black = self.forcing_set - self.passive_black
        self.white = set(range(self.n)) - self.active_black - self.passive_black

    def report_sets(self):
        return {
            "white vertices": list(self.white),
            "active black vertices": list(self.active_black),
            "passive black vertices": list(self.passive_black),
        }

    def simulate_round(self):
        temp_newblack_collector = set()
        for white_node in self.white:
            turning_candidates = self.active_black & self.neighbors[white_node]
            for neighbor in turning_candidates:
                if self.black_neighbor_counter[neighbor] == (len(self.neighbors[neighbor]) - 1):
                    temp_newblack_collector.add(white_node)
                    break

        self.white -= temp_newblack_collector
        self.active_black = self.active_black | temp_newblack_collector

        for new_black_node in temp_newblack_collector:
            for neighbor in self.neighbors[new_black_node]:
                self.black_neighbor_counter[neighbor] += 1
        
        temp_passiveblack_collector = set()
        for node in self.active_black:
            if self.black_neighbor_counter[node] == len(self.neighbors[node]):
                temp_passiveblack_collector.add(node)
        self.active_black -= temp_passiveblack_collector
        self.passive_black = self.passive_black | temp_passiveblack_collector

        return len(temp_newblack_collector)

    def simulate_forcing(self):
        round_counter = 0
        new_vertex_forced = True
        while new_vertex_forced:
            new_vertex_forced = self.simulate_round()
            round_counter += 1
            logger.debug(
                f"Round {round_counter} completed, new vertices forced"
            )
            logger.debug(self.report_sets())
        if self.n == len(self.passive_black):
            logger.debug(f"inital set forced the graph in {round_counter - 1} rounds")
            return (True, round_counter - 1)
        else:
            logger.debug(
               f"Forcing stopped in round {round_counter}, the initial set does not force the graph"
            )
            return (False, round_counter - 1)


def calculate_zero_forcing_nr(neighbors: typing.Dict[int, typing.Set[int]], showMinSets: bool=False):
    minimum_sets = []
    stop_search = False
    for subset_size in range(1, len(neighbors)):
        logger.debug("    -> Checking subsets of size {}".format(subset_size))
        for subset in combinations(range(len(neighbors)), subset_size):
            zf = ZeroForcing(neighbors, set(subset))
            if zf.simulate_forcing()[0]:
                logger.debug(f"minimum forcing set {subset} of size {subset_size} found!")
                minimum_sets.append(subset)
                stop_search = True
        if stop_search:
            if showMinSets:
                logger.info(sorted(minimum_sets))
            logger.debug("Minimum forcing set size {}".format(len(minimum_sets[0])))
            return len(minimum_sets[0])
