import random
import sys
N = 4
K = 20

class Zagadka:
    def __init__(self, seed):
        random.seed(seed)
        self.__haslo = [random.randint(1, K) for i in range(0, N)]

    def to_string(self):
        return str(self.__haslo)

    def basic_compare(self, podejscie):
        poprawne = 0
        for i in range(0, N):
            if self.__haslo[i] == podejscie[i]:
                poprawne += 1
        return poprawne


class Solution:
    def __init__(self, randomly=True, lista_n_elementowa=[]):
        if randomly:
            self.rozwiazanie = [random.randint(1, K) for i in range(0, N)]
        else:
            self.rozwiazanie = lista_n_elementowa

    def mutate(self, position):
        if position>= N or position < 0:
            print('Wskazano zla pozycje', file=sys.stderr)
            return
        self.rozwiazanie[position] = random.randint(1, K)

    def local_search(self, zagadka):
        liczba_iteracji = 0
        while zagadka.basic_compare(self.rozwiazanie) < N:
            self.mutate(random.randint(0, N-1))
            liczba_iteracji += 1
        print(f'rozwiązanie znalezone po: {liczba_iteracji}')