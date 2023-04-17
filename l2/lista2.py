#!/usr/bin/python3.8

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from copy import deepcopy


def assign_flow(graph, matrix):
    nx.set_edge_attributes(graph, 0, "a")
    nodes = nx.number_of_nodes(graph)
    for i in range(nodes):
        for j in range(nodes):
            path = nx.shortest_path(graph, i, j)
            for n in range(len(path) - 1):
                graph[path[n]][path[n + 1]]["a"] += matrix[i][j]


def assign_capacity(graph, matrix):
    nx.set_edge_attributes(graph, 0, "c")
    for i, j in graph.edges:
        graph[i][j]["c"] = graph[i][j]["a"] // 5 * 50 + 50


def T(graph, matrix_sum, m):
    T = 0
    for i, j in graph.edges:
        a = graph[i][j]["a"]
        c = graph[i][j]["c"]
        if a >= c / m:
            return None
        else:
            T += a / (c / m - a)
    return T / matrix_sum


def reliability(graph, matrix, T_max, p, m, iterations=100, intervals=10):
    successful_trials = 0
    matrix_sum = sum(sum(row) for row in matrix)
    base_t = T(graph, matrix_sum, m)
    for _ in range(iterations):
        trial_graph = deepcopy(graph)
        for _ in range(intervals):
            broken = [e for e in nx.edges(trial_graph) if random.random() > p]
            if broken:
                trial_graph.remove_edges_from(broken)
                if not nx.is_connected(trial_graph):
                    break
                assign_flow(trial_graph, matrix)
                t = T(trial_graph, matrix_sum, m)
            else:
                t = base_t
            if not t or t >= T_max:
                break
            successful_trials += 1
    return successful_trials / (iterations * intervals)


def fast_assign_flow(graph, i, j, change):
    path = nx.shortest_path(graph, i, j)
    for n in range(len(path) - 1):
        graph[path[n]][path[n + 1]]["a"] += change


def test1(graph, matrix, T_max, p, m, iterations=10, step=10):
    test_graph = deepcopy(graph)
    test_matrix = deepcopy(matrix)
    results = [reliability(test_graph, test_matrix, T_max, p, m)]
    for _ in range(iterations):
        while True:
            i, j = random.randint(0, 19), random.randint(0, 19)
            if i != j:
                break
        test_matrix[i][j] += step
        fast_assign_flow(test_graph, i, j, step)
        results.append(reliability(test_graph, test_matrix, T_max, p, m))
    return results


def test2(graph, matrix, T_max, p, m, iterations=10):
    test_graph = deepcopy(graph)
    results = [reliability(test_graph, matrix, T_max, p, m)]
    for _ in range(iterations):
        for i, j in test_graph.edges:
            test_graph[i][j]["c"] += 50
        results.append(reliability(test_graph, matrix, T_max, p, m))
    return results


def test3(graph, matrix, T_max, p, m, iterations=10):
    test_graph = deepcopy(graph)
    results = [reliability(test_graph, matrix, T_max, p, m)]
    caps = nx.get_edge_attributes(test_graph, "c").values()
    new_cap = sum(caps) / len(caps)
    non_nodes = list(nx.non_edges(test_graph))
    for _ in range(iterations):
        i, j = random.sample(non_nodes, 1)[0]
        non_nodes.remove((i, j))
        test_graph.add_edge(i, j)
        test_graph[i][j]["c"] = new_cap
        assign_flow(test_graph, matrix)
        results.append(reliability(test_graph, matrix, T_max, p, m))
    return results


def main():
    G = nx.disjoint_union(nx.cycle_graph(9), nx.cycle_graph(11))
    for i in range(9):
        G.add_edge(i, i + 10)

    N = []
    for i in range(20):
        N.append([])
        for j in range(20):
            if i == j:
                N[i].append(0)
            else:
                N[i].append(random.randint(1, 9))
    print(np.matrix(N))

    assign_flow(G, N)
    assign_capacity(G, N)

    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos)
    nx.draw_networkx_labels(G, pos, font_color="w")
    nx.draw(G, pos)
    plt.show()

if __name__ == "__main__":
    main()
