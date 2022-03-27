from utils.ToolBox import graph_from_edges
from ProblemA import *
from ProblemB import *
# from utils.tests import *
from time import time

if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                                     directed=False, drop_rows=4)
    # time_start = time()
    # population = Population(population_size=100,
    #                         cooperation_graph=graph)
    # print(f"Population created, exec time: {time() - time_start}")
    # population.solve_problem(p_cross=0.5, p_mutation=0.01, time_limit=60)

    # graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    # print(len(graph))
    graph.pop(12295)
    city = City(graph, 1000)
    time_start = time()
    city.start_searching(stop_time=10, p_start_size=0.1)
    print(f'Cover size: {len(city.current_cover)}, time: {time() - time_start}')
    print(f'Is cover good: {city.check_cover()}')

