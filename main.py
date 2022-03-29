from utils.ToolBox import graph_from_edges
from ProblemA import *
# from ProblemACython import *
from ProblemB import *
from time import time
# from utils.tests import *


def param_test_problem_a():
    global graph, file_log, text_log
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=False, drop_rows=4)
    file_log = open('output/log_problemA.txt', 'w')
    for cross in [0.1, 0.2, 0.5, 0.75, 1]:
        for mutation in [0.001, 0.01, 0.1, 0.25]:
            for size in [10, 50, 100, 200]:
                time_start = time()
                population = Population(population_size=size,
                                        cooperation_graph=graph)
                population.solve_problem(p_cross=cross,
                                         p_mutation=mutation, time_limit=10)
                text_log = f"Problem solved, result score: {population.list[0].group_size}, " \
                           f"exec time: {time() - time_start}, p_cross: {cross}, p_mutation: {mutation}, " \
                           f"population_size: {size}, best group:\n{population.list[0].members}\n"
                print(text_log)
                file_log.write(text_log)
    file_log.close()


def param_test_problem_b():
    global graph, file_log, text_log
    graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    file_log = open('output/log_problemB.txt', 'w')
    best_cover = list(graph.keys())
    for qsize in [1e4, 1e6, 1e10]:
        for start_size in [0.01, 0.1, 0.25, 0.5, 0.75]:
            for stop_time in [10, 20, 30]:
                city = City(graph, max_qsize=qsize)
                city.start_searching(stop_time=stop_time,
                                     p_start_size=start_size)
                text_log = f'Problem solved, result score: {len(city.current_cover)}, ' \
                           f'stop_time: {stop_time}, p_start_size: {start_size}, max_qsize: {qsize}, ' \
                           f'Is cover good?: {city.check_cover()}\n'
                print(text_log)
                file_log.write(text_log)
                if len(best_cover) > len(city.current_cover):
                    best_cover = list(city.current_cover)
    file_log.write(f'BEST BEST cover: {best_cover}')
    file_log.close()


if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=False, drop_rows=4)
    population = Population(population_size=100,
                            cooperation_graph=graph)
    population.solve_problem(p_cross=1,
                             p_mutation=0.01, time_limit=10)

    # graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    # city = City(graph, 1e10)
    # time_start = time()
    # city.start_searching(stop_time=900, p_start_size=0.1)
    # print(f'Cover size: {len(city.current_cover)}, time: {time() - time_start}')
    # print(f'Is cover good: {city.check_cover()}')

    # param_test_problem_a()
    # param_test_problem_b()

    # test_group_speed(graph)