import random
import time
from queue import SimpleQueue
from copy import deepcopy
from collections import deque

import numpy as np


class Population:
    def __init__(self, population_size, cooperation_graph):
        """Tworzymy populacje jako liste objektow Group"""
        self.available_id = set(cooperation_graph.keys())
        self.list = [Group(cooperation_graph=cooperation_graph,
                           group_size=random.randint(1, len(self.available_id)))
                     for i in range(population_size)]
        self.cooperation_graph = cooperation_graph
        self.population_size = population_size
        self.best_group_weight = 0

    def evaluate(self):
        """Ewaluacja wszystkich osobnikow w populacji"""
        eval_list = [group.weight for group in self.list]
        return eval_list

    def cross(self, parent1, parent2):
        """Krzyzowanie dwoch osobnikow"""
        set1 = set(random.sample(parent1.members, int(parent1.group_size / 2)))
        set2 = set(random.sample(parent2.members, int(parent2.group_size / 2)))
        child = Group(self.cooperation_graph,
                      members=set.union(set1, set2))
        return child

    def cross_all(self, cross_p):
        """Skrzyzowanie wszystkich osobnikow"""
        random.shuffle(self.list)
        to_cross = self.list[:int(len(self.list)*cross_p)]
        N = len(to_cross)
        children = []
        if N % 2 == 0:
            for parent1, parent2 in zip(to_cross[:int(N/2)], to_cross[int(N/2):]):
                children.append(self.cross(parent1, parent2))
        else:
            for parent1, parent2 in zip(to_cross[:int((N-1)/2)], to_cross[int((N-1)/2):-1]):
                children.append(self.cross(parent1, parent2))
        return children

    def update_population(self, cross_p=1):
        """Wykonujemy iteracje, czyli rozmnzazamy i ewaloujemy nasza populacje"""
        kids = self.cross_all(cross_p)
        new_population = self.list + kids
        new_population.sort(key=lambda x: x.weight, reverse=True)
        self.list = new_population[:self.population_size]
        self.best_group_weight = self.list[0].weight


class Group:
    """Klasa Group przechowuje liste id czonkow grupy araz posiada metody do
    ewaluacji i mutacji grupy"""

    def __init__(self, cooperation_graph, group_size=None, members=None,
                 mutation_frequency=0.1):
        available_id = set(cooperation_graph.keys())
        if members is None:
            self.members = random.sample(available_id, group_size)
            self.group_size = group_size
            self.weight = self.evaluate(cooperation_graph)
        elif group_size is None:
            self.members = members
            self.group_size = len(members)
            self.mutate(available_id, mutation_frequency)
            self.weight = self.evaluate(cooperation_graph)

    def evaluate(self, cooperation):
        """Liczymy ile jest osob w grupie a potem odejmujemy punkty za kazda
        osobe ktora wspolpracowala z kims z grupy"""
        # temp_members = self.members.copy()
        # for member1 in temp_members:
        #     for member2 in temp_members:
        #         if member1 in cooperation[member2] and member1 != member2:
        #             self.members.remove(member1) #wyrzucamy ludzi jesli ze soba pracowali
        #             break
        temp = {x: y for x, y in cooperation.items() if x in self.members}
        not_allowed = set().union(*temp.values())
        for m in not_allowed:
            if m in self.members:
                self.members.remove(m)

        weight = len(self.members)
        self.group_size = weight
        return weight

    def mutate(self, available_id, p=0.1):
        """Tworzymy losowe mutacje w grupie z prawdopodobienstwem p"""
        N = int(self.group_size * p)
        indexes = random.sample(range(self.group_size), N)
        new_gens = random.sample(available_id, N)
        temp = list(self.members)
        for x, y in zip(indexes, new_gens):
            temp[x] = y
        self.members = set(temp)


###############################################################################
# Zadanie 1 czesc B
class City:
    def __init__(self, graph, max_qsize):
        self.vertexes = list(graph.keys())
        self.general_graph = graph
        self.current_cover = graph
        self.number_vertexes = len(graph)
        self.max_qsize = max_qsize
        self.tabu_list = deque()
        self.tabu_list.appendleft(set(graph.keys()))

    def start_searching(self, stop_time):
        time_start = time.time()
        i = 0
        while True:
            self.get_better_neighbour()
            i += 1
            if (time.time() - time_start) > stop_time:
                break
        print(f'Number of interations: {i}')
        return self.current_cover

    def check_cover(self, graph):
        seen_vertexes = set().union(*graph.values())
        return len(seen_vertexes) == self.number_vertexes

    def get_better_neighbour(self):
        new_cover = None
        for i in range(self.number_vertexes):
            v_from = random.sample(self.current_cover.keys(), 1)[0]
            v_to = random.sample(self.general_graph[v_from], 1)[0]
            if self.check_move_possibility(v_from, v_to):
                new_cover = self.move_vertex(self.current_cover, v_from, v_to)
                break
        else:
            print('Nie znaleziono możliwego ruchu')

        if new_cover is not None and len(new_cover) < len(self.current_cover):
            self.current_cover = deepcopy(new_cover)
        if len(self.tabu_list) > self.max_qsize:
            self.tabu_list.pop()
        self.tabu_list.appendleft(set(new_cover.keys()))

    def move_vertex(self, graph, v_from, v_to):
        new_graph = deepcopy(graph)
        new_graph.pop(v_from)
        new_graph[v_to] = self.general_graph[v_to]
        return new_graph

    def check_move_possibility(self, v_from, v_to):
        neighbours = set().union(*{x: y for x, y in self.general_graph.items() if x in self.general_graph[v_from]}.values())
        for neighbour in neighbours:
            if len(self.current_cover[neighbour]) <= 1:
                if neighbour in self.general_graph[v_to]:
                    new_cover = set(self.current_cover.keys())
                    new_cover.remove(v_from)
                    new_cover.add(v_to)
                    if new_cover in self.tabu_list:
                        return False
                    else:
                        return True
                else:
                    return False
        new_cover = set(self.current_cover.keys())
        new_cover.remove(v_from)
        new_cover.add(v_to)
        if new_cover in self.tabu_list:
            return False
        else:
            return True
