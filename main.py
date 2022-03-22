from ToolBox import graph_from_edges
from Zadanie1 import *
from time import time


if __name__ == '__main__':
    # graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
    #                                  directed=True, drop_rows=4)
    # time_start = time()
    # population = Population(100, graph)
    # print(f"Population created, exec time: {time() - time_start}")
    # population.solve_problem()


    graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    # print(len(graph))
    #
    city = City(graph, 1000)
    time_start = time()
    # city.random_cover()
    city.start_searching(30)
    print(f'Cover size: {len(city.current_cover)}, time: {time() - time_start}')
    print(f'Is cover good: {city.check_cover()}')

    # print(f'Problem solved, found cover with {len(city.start_searching(stop_time=20))} vertexes')
