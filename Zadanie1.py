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
        self.general_graph = graph  # wyjściowy graf
        self.vertexes = set(graph.keys())  # zbió wszystkich wierzcholków

        # self.how_many_looking = {x: len(graph[x]) for x in graph}
        # self.current_cover = set(graph.keys())
        self.how_many_looking = None  # ile wiercholków z pokrycia 'patrzy' na dany wierzchołek
        self.current_cover = None  # aktualne pokrycie wierzchołkowe

        self.number_vertexes = len(graph)  # liczba wszystkich wierzchołków
        self.max_qsize = max_qsize  # maksymalny rozmiar listy tabu
        self.tabu_list = deque()  # lista tabu w postaci deque
        # self.tabu_list.appendleft(set(graph.keys()))

    def start_searching(self, stop_time):
        """Zaczynamy szukac rozwiazania, startujemy od randomowego pokrycia"""
        self.random_cover()
        time_start = time.time()
        i = 0
        while True:
            # wyszukujemy lepszego rozwiazania w poblizu
            self.get_better_neighbour()
            i += 1
            if (time.time() - time_start) > stop_time: # warunek stopu
                break
        print(f'Number of interations: {i}')
        return self.current_cover

    def check_cover(self, cover=None):
        """Sprawdzamy czy dany zbiór jest rzeczywiście pokryciem wierzchołkowym"""
        if cover is None:
            cover = self.current_cover
        seen_vertexes = set().union(*{x: y for x, y in self.general_graph.items() if x in cover}.values())
        seen_vertexes = seen_vertexes.union(cover)
        return len(seen_vertexes) == self.number_vertexes

    def get_better_neighbour(self):
        """Szukamy lepszego rozwiązania w pobliżu które nie jest na liście tabu"""
        for i in range(self.number_vertexes):
            v_from = random.sample(self.current_cover, 1)[0]
            v_to = random.sample(self.general_graph[v_from], 1)[0]
            if self.check_move_possibility(v_from, v_to):
                self.move_vertex(self.current_cover, v_from, v_to)
                break
        else:
            print('Nie znaleziono możliwego ruchu')

        # Resize listy tabu
        if len(self.tabu_list) > self.max_qsize:
            self.tabu_list.pop()


    def move_vertex(self, v_set, v_from, v_to):
        """Usunięcie wierzchołka lub przeniesienie wierzcholka z listy pokrycia"""
        new_cover = v_set.copy()
        new_cover.remove(v_from)
        for v in self.general_graph[v_from]:
            self.how_many_looking[v] -= 1
        new_cover.add(v_to)
        for v in self.general_graph[v_to]:
            self.how_many_looking[v] += 1
        # Jeśli nowe rozwiązanie jest lepsze to nadpisujemy
        if len(new_cover) < len(self.current_cover):
            self.current_cover = new_cover
        self.tabu_list.appendleft(new_cover)

    def check_move_possibility(self, v_from, v_to):
        """Sprawdzamy czy dany ruch jest dopuszczalny, czyli czy dane rozwiązanie
        znajduje się na liście rozwiązań dopuszczalnych"""
        # TODO: dodać sprawdzenie czy rozwiąznie jest na lisćie tabu!
        for neighbour in self.general_graph[v_from]:
            if self.how_many_looking[neighbour] <= 1:
                if neighbour in self.general_graph[v_to]:
                    return True
                else:
                    return False
        return True

    def random_cover(self):
        """Losowanie zbioru i dsotosowanie go tak aby był pokryciem wierzchołkowym"""
        cover = set(random.sample(self.general_graph.keys(),
                                  int(self.number_vertexes/2)))
        how_many_looking = {x: 0 for x in self.vertexes}
        for vertex in cover:
            how_many_looking[vertex] += 1
            for neighbour in self.general_graph[vertex]:
                how_many_looking[neighbour] += 1
        # Zbiór jaki trzeba uzupełnić żeby to było pokrycie  wierzchołkowe
        to_add = set(x for x in self.vertexes if how_many_looking[x] <= 0)
        for vertex in to_add:
            if how_many_looking[vertex] <= 0:
                cover.add(vertex)
                how_many_looking[vertex] += 1
                for neighbour in self.general_graph[vertex]:
                    how_many_looking[neighbour] += 1
        self.how_many_looking = how_many_looking
        self.current_cover = cover
        self.tabu_list.appendleft(cover)
