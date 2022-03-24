import random
from time import time
from ProblemA import Group
import pyximport
pyximport.install()
import ProblemACython


def test_group_speed(graph):
    size = len(graph)
    random.seed(123)
    time_start = time()

    population = [Group(cooperation_graph=graph,
                        group_size=random.randint(1, size)) for i in range(50)]
    print(f'Population created, exec time: {time() - time_start}')
    time_start = time()

    population2 = [ProblemACython.Group(cooperation_graph=graph,
                                        group_size=random.randint(1, size))
                   for i in range(50)]
    print(f'Population created, exec time: {time() - time_start}')

