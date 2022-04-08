from utils.ToolBox import graph_from_edges
from ProblemA import *
# from ProblemACython import *
from ProblemB import *
from time import time
# from utils.tests import *


if __name__ == '__main__':
    graph = graph_from_edges('data/Arxiv_GR_collab_network.txt',
                             directed=False, drop_rows=4)
    population = Population(population_size=1000,
                            cooperation_graph=graph)
    population.solve_problem(p_cross=1,
                             p_mutation=0.01, time_limit=10)

    graph = graph_from_edges('data/roadNet_USRoads.txt', drop_rows=16)
    city = City(graph, 1e10)
    time_start = time()
    city.start_searching(stop_time=900, p_start_size=0.1)
    print(f'Cover size: {len(city.current_cover)}, time: {time() - time_start}')
    print(f'Is cover good: {city.check_cover()}')

    # param_test_problem_a()
    # param_test_problem_b()
