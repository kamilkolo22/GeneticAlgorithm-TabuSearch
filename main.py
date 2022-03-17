from Labki1 import Zagadka, Solution
from ToolBox import graph_from_edges
from Zadanie1 import *
from time import time


def start_problem_A():
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=True, drop_rows=4)
    time_start = time()
    population = Population(100, graph)
    print(f"Population created, exec time: {time() - time_start}")
    generation_number = 0
    best_weight = 0
    flag = 0
    while True:
        population.update_population(cross_p=1)
        generation_number += 1
        temp = population.best_group_weight
        if flag == 20:
            break
        elif best_weight >= temp:
            flag += 1
        else:
            best_weight = temp
            flag = 0
    print(f'Best group: {population.list[0]} \n'
          f'Size: {population.list[0].group_size} \n'
          f'Number of generation: {generation_number} \n'
          f'Execution time: {time()-time_start}')


if __name__ == '__main__':
    start_problem_A()
    # graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    #
    # city = City(graph)
    # time_start = time()
    # city.check_cover()
    # print(f"{time() - time_start}")

