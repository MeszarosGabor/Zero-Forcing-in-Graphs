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

def get_level_n_binary_pendant_neighbors(level):
    if level == 1:
        return level_1_binary_pendant_neighbors
    smaller = get_level_n_binary_pendant_neighbors(level - 1)
    smaller_size = len(smaller)
    left = deepcopy(smaller)
    left[smaller_size // 2].add(smaller_size)
    right = shift_pendant_indexes(smaller, smaller_size + 1)
    right[smaller_size // 2].add(smaller_size)
    return left + [{smaller_size // 2, smaller_size + smaller_size // 2 + 1}] + right
