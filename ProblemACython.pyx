import random
import time
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)


cdef class Group:
    """Klasa Group przechowuje liste id czonkow grupy araz posiada metody do
    ewaluacji i mutacji grupy"""
    cdef public set members;
    cdef public int group_size;
    cdef public float weight;

    def __init__(self, cooperation_graph, group_size=None,
                 members=None, mutation_frequency=0.1):
        cdef set available_id = set(cooperation_graph.keys());

        if members is None:
            self.members = set(random.sample(available_id, group_size))
            self.group_size = group_size
            self.weight = self.evaluate(cooperation_graph)
        elif group_size is None:
            self.members = members
            self.group_size = len(members)
            self.mutate(available_id, mutation_frequency)
            self.weight = self.evaluate(cooperation_graph)

    cdef float evaluate(self, dict cooperation):
        """Liczymy ile jest osob w grupie a potem odejmujemy punkty za kazda
        osobe ktora wspolpracowala z kims z grupy"""
        cdef int weight = len(self.members);
        cdef dict temp;

        temp = {x: y for x, y in cooperation.items() if x in self.members}
        not_allowed = set().union(*temp.values())
        for m in not_allowed:
            if m in self.members:
                weight -= 1

        return weight

    cdef void mutate(self, set available_id, float p=0.1):
        """Tworzymy losowe mutacje w grupie z prawdopodobienstwem p"""
        cdef int N;
        cdef list indexes, new_gens, temp;

        N = int(self.group_size * p)
        indexes = random.sample(range(self.group_size), N)
        new_gens = random.sample(available_id, N)
        temp = list(self.members)
        cdef int i;
        for i in range(N):
            temp[indexes[i]] = new_gens[i]
        self.members = set(temp)

    def adjust_result(self, cooperation):
        temp_members = self.members.copy()
        for member1 in temp_members:
            for member2 in temp_members:
                if member1 in cooperation[member2] and member1 != member2:
                    self.members.remove(
                        member1)  # wyrzucamy ludzi jesli ze soba pracowali
                    break
        self.group_size = len(self.members)
        self.weight = self.evaluate(cooperation)
        return self.members


cdef class Population:
    cdef set available_id;
    cdef list list;
    cdef dict cooperation_graph;
    cdef int population_size;
    cdef float best_group_weight;

    def __init__(self, population_size, cooperation_graph):
        """Tworzymy populacje jako liste objektow Group"""
        self.available_id = set(cooperation_graph.keys())
        self.list = [Group(cooperation_graph=cooperation_graph,
                           group_size=random.randint(1, len(self.available_id)))
                     for _ in range(population_size)]
        self.cooperation_graph = cooperation_graph
        self.population_size = population_size
        self.best_group_weight = 0

    def solve_problem(self, p_cross=0.5, p_mutation=0.1, time_limit=None):
        time_start = time.time()
        generation_number = 0
        best_weight = 0
        temp = 1
        flag = 0
        while True:
            if time_limit is None:
                if flag == 5:
                    break
                elif best_weight >= temp:
                    flag += 1
                else:
                    best_weight = temp
                    flag = 0
            else:
                if (time.time() - time_start) > time_limit:
                    break
            self.update_population(p_cross=p_cross, p_mutation=p_mutation)
            generation_number += 1
            # szacujemy
            temp = sum([x.weight for x in self.list]) / len(self.list)
            print(f'average weight: {temp}')

        self.list[0].adjust_result(self.cooperation_graph)
        print(f'Size: {self.list[0].group_size} \n'
              f'Number of generation: {generation_number} \n'
              f'Execution time: {time.time() - time_start}\n'
              f'Best group: \n{self.list[0].members} \n')

    cdef Group cross(self, parent1, parent2, p_mutation=0.1):
        """Krzyzowanie dwoch osobnikow"""
        cdef set set1, set2;
        cdef Group child;

        set1 = set(random.sample(parent1.members, int(parent1.group_size / 2)))
        set2 = set(random.sample(parent2.members, int(parent2.group_size / 2)))
        child = Group(self.cooperation_graph,
                      members=set.union(set1, set2),
                      mutation_frequency=p_mutation)
        return child

    def cross_all(self, p_cross=1.0, p_mutation=0.1):
        """Skrzyzowanie wszystkich osobnikow"""
        random.shuffle(self.list)
        to_cross = self.list[:int(len(self.list) * p_cross)]
        N = len(to_cross)
        children = []
        if N % 2 == 0:
            for parent1, parent2 in zip(to_cross[:int(N/2)], to_cross[int(N/2):]):
                children.append(self.cross(parent1, parent2, p_mutation))
        else:
            for parent1, parent2 in zip(to_cross[:int((N-1)/2)], to_cross[int((N-1)/2):-1]):
                children.append(self.cross(parent1, parent2, p_mutation))
        return children

    def update_population(self, p_cross=1.0, p_mutation=0.1):
        """Wykonujemy iteracje, czyli rozmnzazamy i ewaloujemy nasza populacje"""
        kids = self.cross_all(p_cross, p_mutation)
        new_population = self.list + kids
        new_population.sort(key=lambda x: x.weight, reverse=True)
        self.list = new_population[:self.population_size]
        self.best_group_weight = self.list[0].weight
