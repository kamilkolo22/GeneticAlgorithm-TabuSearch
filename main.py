from utils.ToolBox import graph_from_edges
from ProblemA import *
from ProblemB import *
# from utils.tests import *
from time import time

if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt', directed=False, drop_rows=4)
    file_log = open('output/log_problemA.txt')

    for cross in [0.1, 0.2, 0.5, 0.75, 1]:
        for mutation in [0.001, 0.01, 0.1, 0.25]:
            for size in [10, 50, 100, 200]:
                time_start = time()
                population = Population(population_size=size,
                                        cooperation_graph=graph)
                population.solve_problem(p_cross=cross, p_mutation=mutation, time_limit=10)
                file_log.write(f"Problem solved, result score: {population.list[0].group_size}, "
                               f"exec time: {time() - time_start}, p_cross: {cross}, p_mutation{mutation}, "
                               f"population_size: {population}, best group:\n{population.list[0].members}\n")
    file_log.close()

    graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    file_log = open('output/log_problemB.txt')
    for qsize in [1e3, 1e4, 1e5]:
        for start_size in [0.1, 0.25, 0.5, 0.75]:
            for stop_time in [10, 20, 30]:
                city = City(graph, max_qsize=qsize)
                city.start_searching(stop_time=stop_time, p_start_size=start_size)
                file_log.write(f'Problem solved, result score: {len(city.current_cover)}, '
                               f'stop_time: {stop_time}, p_start_size: {start_size}, max_qsize: {qsize}, '
                               f'Is cover good?: {city.check_cover()}, best cover:\n{city.current_cover}\n')
    file_log.close()

    # graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    # print(len(graph)
    # graph.pop(12295)
    # city = City(graph, 1000)
    # time_start = time()
    # city.start_searching(stop_time=10, p_start_size=0.1)
    # print(f'Cover size: {len(city.current_cover)}, time: {time() - time_start}')
    # print(f'Is cover good: {city.check_cover()}')
