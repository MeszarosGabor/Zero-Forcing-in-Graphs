# Zero-Forcing-in-Graphs
Implementation of the zero forcing process in graphs.
See http://www.memphis.edu/msci/people/gmszaros/on_a_conjecture_of_gentner_and_rautenbach.pdf



# TODOs and additional remarks
- Remove all print statements. Apply decent logging schemas. (DONE)
- Fix and add typing. (DONE)
- searcher is way to big. Move supporting functionalities into a utils.py
- Major refactor to simplify the graph repr handling using networkx objects whenever reasonable.
    --> This might cause difficulties at persistence (must pickle the Graph object)
    --> This might cause performance issues (must investigate vanilla repr vs networkx)

- 
