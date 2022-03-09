import random
import sys
N = 4
K = 20

class Solution:
    def __init__(self, randomly=True, lista_n_elementowa=[]):
        if (randomly):
            self.rozwiazanie = [random.randint(1, K) for i in range(0, N)]

        else:
            self.rozwiazanie = lista_n_elementowa

    def mutate(self, position):
        if (position >= N or position < 0):
            print("Wskazano złą pozycję ", file=sys.stderr)
            return
        self.previous_position = position
        self.previous_value = self.rozwiazanie[position]
        self.rozwiazanie[position] = random.randint(1, K)

    def mutate(self, position, list_of_unused_values):
        if (position >= N or position < 0):
            print("Wskazano złą pozycję ", file=sys.stderr)
            return
        self.previous_position = position
        self.previous_value = self.rozwiazanie[position]
        self.rozwiazanie[position] = random.choice(list_of_unused_values)

    def reverse_mutation(self):
        self.rozwiazanie[self.previous_position] = self.previous_value

    def local_search(self, zagadka):
        liczba_iteracji = 0

        while (zagadka.basic_compare(self.rozwiazanie) < N):
            self.mutate(random.randint(0, N - 1))
            liczba_iteracji += 1
        print("Rozwiązanie znalezione po ", liczba_iteracji, " iteracjach")

    def iterated_local_search(self, zagadka):
        liczba_iteracji = 0

        current_value = zagadka.basic_compare(self.rozwiazanie)
        while (current_value < N):
            self.mutate(random.randint(0, N - 1))
            liczba_iteracji += 1
            new_value = zagadka.basic_compare(self.rozwiazanie)
            if (new_value >= current_value):
                current_value = new_value
            else:
                self.reverse_mutation()
        print("Rozwiązanie znalezione po ", liczba_iteracji, " iteracjach")

    def fixed_pos_ILS(self, zagadka):
        liczba_iteracji = 0

        current_value = zagadka.basic_compare(self.rozwiazanie)
        list_of_indices = [i for i in range(0, N)]
        while (current_value < N):
            self.mutate(random.choice(list_of_indices))
            liczba_iteracji += 1
            new_value = zagadka.basic_compare(self.rozwiazanie)
            if (new_value >= current_value):
                current_value = new_value
            else:
                list_of_indices.remove(self.previous_position)
                self.reverse_mutation()
        print("Rozwiązanie znalezione po ", liczba_iteracji, " iteracjach")

    def perfected_ILS(self, zagadka):
        liczba_iteracji = 0

        current_value = zagadka.basic_compare(self.rozwiazanie)
        pos = 0
        list_of_values = [i for i in range(0, K)]
        list_of_values.remove(self.rozwiazanie[pos])
        while (pos < N):
            liczba_iteracji += 1
            self.mutate(pos, list_of_values)
            new_value = zagadka.basic_compare(self.rozwiazanie)
            if (new_value > current_value):
                list_of_values = [i for i in range(0, K)]
                current_value = new_value
                pos += 1
            elif (new_value < current_value):
                list_of_values = [i for i in range(0, K)]
                self.reverse_mutation()
                pos += 1
            else:
                list_of_values.remove(self.rozwiazanie[pos])
    # The last case involves the situation where the introduced change guessed wrong.
                continue
        print("Rozwiązanie znalezione po ", liczba_iteracji, " iteracjach")

class Population(Solution):
    def __init__(self, number):
        super(Population, self).__init__()

    def cross(self, parent1, parent2):
        child = parent1[:N//2] + parent2[N//2:]
        return child

    def mutate(self, person):
        pos = randint(self.number)
        mutated = person.copy()
        mutated[pos] = randint(1, N)
        return mutated


