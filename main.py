from Labki1 import Zagadka, Solution
from ToolBox import graph_from_edges
from Zadanie1 import *


if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=True, drop_rows=4)
    population = Population(30, graph)

    best_weight = 0
    flag = 0
    while True:
        population.update_population()
        temp = population.best_group_weight
        if flag == 5:
            break
        elif best_weight >= temp:
            flag += 1
        else:
            best_weight = temp
            flag = 0

    print(f'Best group: {population.list[0]} \n'
          f'Weight: {population.best_group_weight}\n'
          f'Admissible: {population.list[0].is_group_admissible()}\n'
          f'Size: {population.list[0].group_size}')

