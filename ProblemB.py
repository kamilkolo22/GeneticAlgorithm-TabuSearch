import random
import time
from collections import deque


class City:
    def __init__(self, graph, max_qsize):
        self.general_graph = graph  # wyjściowy graf
        self.vertexes = set(graph.keys())  # zbiór wszystkich wierzcholków

        self.how_many_looking = None  # ile wiercholków z pokrycia 'patrzy' na dany wierzchołek
        self.current_cover = None  # aktualne pokrycie wierzchołkowe

        self.number_vertexes = len(graph)  # liczba wszystkich wierzchołków
        self.max_qsize = max_qsize  # maksymalny rozmiar listy tabu
        self.tabu_list = deque()  # lista tabu w postaci deque

    def start_searching(self, stop_time, p_start_size=0.5):
        """Zaczynamy szukac rozwiazania, startujemy od randomowego pokrycia"""
        self.random_cover(p_size=p_start_size)
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
        for neighbour in self.general_graph[v_from]:
            if self.how_many_looking[neighbour] <= 1:
                if neighbour in self.general_graph[v_to]:
                    return self.check_tabu_list(v_from, v_to)
                else:
                    return False
        return self.check_tabu_list(v_from, v_to)

    def check_tabu_list(self, v_from, v_to):
        new_cover = self.current_cover.copy()
        new_cover.remove(v_from)
        new_cover.add(v_to)
        if new_cover in self.tabu_list:
            return False
        else:
            return True

    def random_cover(self, p_size=0.5):
        """Losowanie zbioru i dsotosowanie go tak aby był pokryciem wierzchołkowym"""
        cover = set(random.sample(self.general_graph.keys(),
                                  int(self.number_vertexes * p_size)))
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
