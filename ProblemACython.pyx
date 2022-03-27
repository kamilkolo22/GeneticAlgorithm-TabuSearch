import random

#@cython.boundscheck(False)
#@cython.wraparound(False)


class Group:
    """Klasa Group przechowuje liste id czonkow grupy araz posiada metody do
    ewaluacji i mutacji grupy"""

    def __init__(self, cooperation_graph, group_size=None,
                 members=None,float mutation_frequency=0.1):
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
        cdef int weight;

        temp = {x: y for x, y in cooperation.items() if x in self.members}
        not_allowed = set().union(*temp.values())
        for m in not_allowed:
            if m in self.members:
                self.members.remove(m)

        weight = len(self.members)
        self.group_size = weight
        return weight

    def mutate(self, available_id,float p=0.1):
        """Tworzymy losowe mutacje w grupie z prawdopodobienstwem p"""
        cdef int N;

        N = int(self.group_size * p)
        indexes = random.sample(range(self.group_size), N)
        new_gens = random.sample(available_id, N)
        temp = list(self.members)
        for x, y in zip(indexes, new_gens):
            temp[x] = y
        self.members = set(temp)
