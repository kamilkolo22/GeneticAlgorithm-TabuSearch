import random
import numpy as np


class Population:
    def __init__(self, population_size, cooperation_graph):
        self.available_id = set(cooperation_graph.keys())
        self.list = [Group(cooperation_graph=cooperation_graph,
                           group_size=random.randint(1, len(self.available_id)))
                     for i in range(population_size)]
        self.cooperation_graph = cooperation_graph

    def evaluate(self):
        eval_list = [group.weight for group in self.list]
        return eval_list

    def cross(self, parent1, parent2):
        set1 = set(random.sample(parent1.members, int(parent1.group_size / 2)))
        set2 = set(random.sample(parent2.members, int(parent2.group_size / 2)))
        child = Group(self.cooperation_graph,
                      members=set.union(set1, set2))
        return child

    def cross_all(self):
        random.shuffle(self.list)
        N = len(self.list)
        childs = []
        if N == 0:
            for parent1, parent2 in self.list[:N/2], self.list[N/2:]:
                childs.append(self.cross(parent1, parent2))
        else:
            for parent1, parent2 in self.list[:int((N-1)/2)], self.list[int((N-1)/2):-1]:
                childs.append(self.cross(parent1, parent2))
        return childs

class Group:
    def __init__(self, cooperation_graph, group_size=None, members=None):
        if members is None:
            available_id = set(cooperation_graph.keys())
            self.members = random.sample(available_id, group_size)
            self.weight = self.evaluate(cooperation_graph)
            self.group_size = group_size
        elif group_size is None:
            self.members = members
            self.group_size = len(members)
            self.weight = self.evaluate(cooperation_graph)

    def evaluate(self, cooperation):
        weight = len(self.members)
        for member1 in self.members:
            for member2 in self.members:
                if member1 != member2 and member1 in cooperation[member2]:
                    weight -= 1
        return weight

    def is_group_admissible(self):
        if self.group_size == self.weight:
            return True
        else:
            return False
