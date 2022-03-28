import random
from time import time
from ProblemA import Group, Population
import pyximport
pyximport.install()
import ProblemACython
from utils.ToolBox import graph_from_edges

# graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
#                                      directed=False, drop_rows=4)


def test_group_speed(graph):
    random.seed(123)

    time_start = time()
    population = Population(population_size=100,
                            cooperation_graph=graph)
    population.update_population()
    time1 = time() - time_start
    print(f'Population updated, exec time: {time1}')
    time_start = time()

    population = ProblemACython.Population(population_size=100,
                                           cooperation_graph=graph)
    population.update_population()
    time2 = time() - time_start
    print(f'Population updated, exec time: {time2}')
    print(f'poprawa: {(time1 - time2)/time1 * 100}%')

# def test_group_py():
#     random.seed(123)
#     population = [Group(cooperation_graph=graph,
#                         group_size=random.randint(1, 1000)) for i in range(10)]
#
# def test_group_pyx():
#     random.seed(123)
#     population = [ProblemACython.Group(cooperation_graph=graph,
#                                        group_size=random.randint(1, 1000))
#                   for i in range(10)]
