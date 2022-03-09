from Labki1 import Zagadka, Solution
from ToolBox import graph_from_edges
from Zadanie1 import *


if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=True, drop_rows=4)
    population = Population(5, graph)
    # print([m.members for m in population.list])
    print([m.members for m in population.cross_all()])


