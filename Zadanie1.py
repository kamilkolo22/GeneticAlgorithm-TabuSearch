import random
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

    def cross_all(self):
        """Skrzyzowanie wszystkich osobnikow"""
        random.shuffle(self.list)
        N = len(self.list)
        children = []
        if N % 2 == 0:
            for parent1, parent2 in zip(self.list[:int(N/2)], self.list[int(N/2):]):
                children.append(self.cross(parent1, parent2))
        else:
            for parent1, parent2 in zip(self.list[:int((N-1)/2)], self.list[int((N-1)/2):-1]):
                children.append(self.cross(parent1, parent2))
        return children

    def update_population(self):
        """Wykonujemy iteracje, czyli rozmnzazamy i ewaloujemy nasza populacje"""
        kids = self.cross_all()
        new_population = self.list + kids
        new_population.sort(key=lambda x: x.weight, reverse=True)
        self.list = new_population[:self.population_size]
        self.best_group_weight = self.list[0].weight


class Group:
    """Klasa Group przechowuje liste id czonkow grupy araz posiada metody do
    ewaluacji i mutacji grupy"""

    def __init__(self, cooperation_graph, group_size=None, members=None):
        available_id = set(cooperation_graph.keys())
        if members is None:
            self.members = random.sample(available_id, group_size)
            self.group_size = group_size
            self.weight = self.evaluate(cooperation_graph)
        elif group_size is None:
            self.members = members
            self.group_size = len(members)
            self.mutate(available_id)
            self.weight = self.evaluate(cooperation_graph)

    def evaluate(self, cooperation):
        """Liczymy ile jest osob w grupie a potem odejmujemy punkty za kazda
        osobe ktora wspolpracowala z kims z grupy"""
        temp_members = self.members.copy()
        for member1 in temp_members:
            for member2 in temp_members:
                if member1 != member2 and member1 in cooperation[member2]:
                    self.members.remove(member1) # wypierdalamy ludzi jesli ze soba pracowali
                    break
        weight = len(self.members)
        self.group_size = weight
        return weight

    def mutate(self, available_id):
        """Tworzymy losowe mutacje w grupie z prawdopodobienstwem p"""
        p = 0.1
        N = int(self.group_size * p)
        indexes = random.sample(range(self.group_size), N)
        new_gens = random.sample(available_id, N)
        temp = list(self.members)
        for x, y in zip(indexes, new_gens):
            temp[x] = y
        self.members = set(temp)

    def is_group_admissible(self):
        if self.group_size == self.weight:
            return True
        else:
            return False
