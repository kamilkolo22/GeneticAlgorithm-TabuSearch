def graph_from_edges(filename, directed=False, drop_rows=0):
    """Wczytuję graf z pliku tesktowego, który w każdej lini zawiera opis jednej krawędzi oraz waga danej krawedzi"""
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            if drop_rows > 0:
                drop_rows -= 1
                continue
            words = line.split()
            if len(words) == 1:
                add_vertex(graph, int(words[0]))
            elif len(words) == 2:
                if directed:
                    add_arc(graph, (int(words[0]), int(words[1])))
                else:
                    add_edge(graph, (int(words[0]), int(words[1])))
            elif len(words) >= 3:
                if directed:
                    add_arc(graph, (int(words[0]), int(words[1])))
                    graph[words[0]][-1] = (int(words[1]), int(words[2]))
                else:
                    add_edge(graph, (int(words[0]), int(words[1])))
                    graph[words[0]][-1] = (int(words[1]), int(words[2]))
                    graph[words[1]][-1] = (int(words[0]), int(words[2]))
    return graph


def add_vertex(graph, vertex):
    """Nowy wierzcholek do istniejacego grafu"""
    if vertex not in graph:
        graph[vertex] = []


def add_arc(graph, arc):
    """Dodaje nowy luk, graf prosty skierowany"""
    u, v = arc
    add_vertex(graph, u)
    add_vertex(graph, v)
    if v not in graph[u]:
        graph[u].append(v)


def add_edge(graph, edge):
    """Dodaje krawedz do grafu"""
    u, v = edge
    add_vertex(graph, u)
    add_vertex(graph, v)
    if u == v:
        raise ValueError("pętla!")
    if v not in graph[u]:
        graph[u].append(v)
    if u not in graph[v]:
        graph[v].append(u)
