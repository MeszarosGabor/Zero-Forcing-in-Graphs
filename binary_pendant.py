from copy import deepcopy

# simple pendant neighborhood list on 5 vertices:
pendant_neighbors = [{1,2}, {0,3,4}, {0,3,4}, {1,2,4}, {1,2,3}]
pn_size = len(pendant_neighbors)
def shift_pendant_indexes(pendant_neighbors, shift):
    return [set(map(lambda x: x + shift, set_)) for set_ in pendant_neighbors]


level_1_binary_pendant_neighbors =\
    deepcopy(pendant_neighbors) +\
    [{0, pn_size + 1}] +\
    shift_pendant_indexes(pendant_neighbors, pn_size + 1)
level_1_binary_pendant_neighbors[0].add(pn_size)
level_1_binary_pendant_neighbors[pn_size + 1].add(pn_size)
