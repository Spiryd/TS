import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from pick import pick
from copy import deepcopy
import pandas as pd
import seaborn as sns

PING_STANDARD_SIZE = 256


def flow(graph, matrix):
    """Generates flow and assigns it to a Graph from given intensity matrix

    Args:
        graph (networkx Graph): Graph to assign flow to
        matrix (2D Integer List): intensity matrix of Bits per sec for a route for node i to j
    """
    nx.set_edge_attributes(graph, 0, "flow")
    node_count = nx.number_of_nodes(graph)
    for i in range(node_count):
        for j in range(node_count):
            path = nx.shortest_path(graph, i, j)
            for n in range(len(path) - 1):
                graph[path[n]][path[n + 1]]["flow"] += matrix[i][j]


def capacity(graph):
    """Generates capacity and assigns it to a Graph

    Args:
        graph (networkx Graph): Graph to assign capacity to 
    """
    nx.set_edge_attributes(graph, 0, "capacity")
    for i, j in graph.edges:
        graph[i][j]["capacity"] = ((graph[i][j]["flow"] * 10) + PING_STANDARD_SIZE)

def T(graph, matrix_sum, m):
    """Calculates avg. latency of a packet in a given Network

    Args:
        graph (networkx Graph): Graph to calculate from
        matrix_sum (Integer): Sum of all the elements in intensity matrix
        m (Integer): Avg. packet size in bits

    Returns:
        Float: avg. latency of a packet
    """
    T = 0
    #print(matrix_sum)
    for i, j in graph.edges:
        a = graph[i][j]["flow"]
        c = graph[i][j]["capacity"]
        if a >= c / m:
            #print("None")
            return None
        else:
            T += a / (c / m - a)
    #print(T / matrix_sum)
    return T / matrix_sum


def reliability(graph, matrix, T_max, p, m, iterations=100, intervals=10):
    """Tests the reliability of the Network

    Args:
        graph (networkx Graph): Graph to be tested
        matrix (2D Integer List): intensity matrix of Bits per sec for a route for node i to j
        T_max (Integer): latency of a packet 
        p (Float):  probability of an edge not failing
        m (Integer): Avg. packet size in bits
        iterations (int, optional): count of iteration in a test. Defaults to 100.
        intervals (int, optional): number of intervals. Defaults to 10.

    Returns:
        Float: reliability of the Network
    """
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
                flow(trial_graph, matrix)
                t = T(trial_graph, matrix_sum, m)
                #print(t)
            else:
                t = base_t
                #print(t)
            if not t or t >= T_max:
                #print("wrong")
                break
            successful_trials += 1
    return successful_trials / (iterations * intervals)


def append_flow(graph, i, j, change):
    """Adds the change to a route between i and j node 

    Args:
        graph (networkx Graph): Graph to be added
        i (Integer): ID of a Node in Graph from
        j (Integer): ID of a Node in Graph to
        change (Integer): amount do add to a path
    """
    path = nx.shortest_path(graph, i, j)
    for n in range(len(path) - 1):
        graph[path[n]][path[n + 1]]["flow"] += change


def experiment1(graph, matrix, T_max, p, m, iterations=10, step=10):
    """Tests the reliability of a network while incrementing the intencity 

    Args:
        graph (networkx Graph): Graph to be tested
        matrix (2D Integer List): intencity matrix
        T_max (Integer): latency of a packet 
        p (Float):  probability of an edge not failing
        m (Integer): Avg. packet size in bits
        iterations (int, optional): number of itetetatons of the experiment. Defaults to 10.
        step (int, optional): increment of intencity. Defaults to 10.

    Returns:
        List: list of results od the experiment
    """
    test_graph = deepcopy(graph)
    test_matrix = deepcopy(matrix)
    results = [reliability(test_graph, test_matrix, T_max, p, m)]
    for _ in range(iterations):
        while True:
            i, j = random.randint(0, 19), random.randint(0, 19)
            if i != j:
                break
        test_matrix[i][j] += step
        append_flow(test_graph, i, j, step)
        results.append(reliability(test_graph, test_matrix, T_max, p, m))
    return results


def experiment2(graph, matrix, T_max, p, m, iterations=10):
    """Tests the reliability of a network while incementing the capacity

    Args:
        graph (networkx Graph): Graph to be tested
        matrix (2D Integer List): intencity matrix
        T_max (Integer): latency of a packet 
        p (Float): probability of an edge not failing
        m (Integer): Avg. packet size in bits
        iterations (int, optional): number of itetetatons of the experiment. Defaults to 10.

    Returns:
        List: list of results od the experiment
    """
    test_graph = deepcopy(graph)
    results = [reliability(test_graph, matrix, T_max, p, m)]
    for _ in range(iterations):
        for i, j in test_graph.edges:
            test_graph[i][j]["capacity"] += PING_STANDARD_SIZE
        results.append(reliability(test_graph, matrix, T_max, p, m))
    return results


def experiment3(graph, matrix, T_max, p, m, iterations=10):
    """Tests the reliability of a network while adding edges with capacities equal as avg. from the previous network

    Args:
        graph (networkx Graph): Graph to be tested
        matrix (2D Integer List): intencity matrix
        T_max (Integer): latency of a packet 
        p (Float): probability of an edge not failing
        m (Integer): Avg. packet size in bits
        iterations (int, optional): number of itetetatons of the experiment. Defaults to 10.

    Returns:
        List: list of results od the experiment
    """
    test_graph = deepcopy(graph)
    results = [reliability(test_graph, matrix, T_max, p, m)]
    caps = nx.get_edge_attributes(test_graph, "capacity").values()
    new_cap = sum(caps) / len(caps)
    non_nodes = list(nx.non_edges(test_graph))
    for _ in range(iterations):
        i, j = random.sample(non_nodes, 1)[0]
        non_nodes.remove((i, j))
        test_graph.add_edge(i, j)
        test_graph[i][j]["capacity"] = new_cap
        flow(test_graph, matrix)
        results.append(reliability(test_graph, matrix, T_max, p, m))
    return results

def gen_intensity_matrix():
    """Generates a random intensity matrix

    Returns:
        2D Integer List: random intensity matrix
    """
    N = []
    for i in range(20):
        N.append([])
        for j in range(20):
            if i == j:
                N[i].append(0)
            else:
                N[i].append(random.randint(0, 8))
    return N

def t1(G, N):
    suma = sum(sum(r) for r in N)
    M = [1, 2, 3, 4]
    P = [0.90, 0.95, 0.99]
    TMAX = [T(G, suma, i) for i in M]
    for p in P:
        for m in M:
            res = []
            for Tmax in TMAX:
                for i in list(enumerate(experiment1(G, N, Tmax, p, m, step=(PING_STANDARD_SIZE*25), iterations=20))):
                    res.append([Tmax, i[0], i[1]])
            df = pd.DataFrame(res, columns=['Tmax', 'iter', 'res'])
            df = df.pivot("Tmax", "iter", "res")
            sns.heatmap(df, cmap='plasma')
            plt.ylabel("T_max")
            plt.xlabel(f"Iteracja dodawania pakietów przy p={p}, m={m}")
            plt.savefig(f"TEST1_{p}_{m}.png")
            plt.clf()
    


def t2(G, N):
    suma = sum(sum(r) for r in N)
    M = [1, 2, 3, 4]
    P = [0.90, 0.95, 0.99]
    TMAX = [T(G, suma, i) for i in M]
    for p in P:
        for m in M:
            res = []
            for Tmax in TMAX:
                for i in list(enumerate(experiment2(G, N, Tmax, p, m, iterations=20))):
                    res.append([Tmax, i[0], i[1]])
            df = pd.DataFrame(res, columns=['Tmax', 'iter', 'res'])
            df = df.pivot("Tmax", "iter", "res")
            sns.heatmap(df, cmap='plasma')
            plt.ylabel("T_max")
            plt.xlabel(f"Iteracja wzroztu przepustowosci przy p={p}, m={m}")
            plt.savefig(f"TEST2_{p}_{m}.png")
            plt.clf()

def t3(G, N):
    suma = sum(sum(r) for r in N)
    M = [1, 2, 3, 4]
    P = [0.90, 0.95, 0.99]
    TMAX = [T(G, suma, i) for i in M]
    for p in P:
        for m in M:
            res = []
            for Tmax in TMAX:
                for i in list(enumerate(experiment3(G, N, Tmax, p, m, iterations=20))):
                    res.append([Tmax, i[0], i[1]])
            df = pd.DataFrame(res, columns=['Tmax', 'iter', 'res'])
            df = df.pivot("Tmax", "iter", "res")
            sns.heatmap(df, cmap='plasma')
            plt.ylabel("T_max")
            plt.xlabel(f"Iteracja dodawania krawedzi przy p={p}, m={m}")
            plt.savefig(f"TEST3_{p}_{m}.png")
            plt.clf()


def see_graph(G):
    """Generates a visual repesentation of the network

    Args:
        G (networkx Graph): Graph repsenting the network
    """
    plt.figure(figsize=(13, 13))
    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos)
    nx.draw_networkx_labels(G, pos, font_color="w")
    nx.draw(G, pos)
    plt.show()


def main():
    G = nx.Graph()
    for i in range(4):
        for j in range(4):
            G.add_edge((i*5 + j), ((j + i*5) + 1))
    G.add_edge(0, 5)
    G.add_edge(5, 10)
    G.add_edge(10, 15)
    G.add_edge(4, 9)
    G.add_edge(9, 14)
    G.add_edge(14, 19)
    G.add_edge(2, 7)
    G.add_edge(7, 12)
    G.add_edge(12, 17)
    print(G)
    
    N = [
        [0, 2, 8, 4, 7, 8, 2, 7, 3, 4, 7, 6, 1, 7, 1, 5, 3, 6, 2, 7], 
        [7, 0, 6, 6, 2, 3, 0, 4, 3, 0, 7, 3, 8, 6, 5, 3, 0, 2, 1, 6], 
        [0, 8, 0, 7, 8, 1, 6, 8, 7, 2, 1, 8, 7, 3, 0, 0, 6, 1, 4, 4], 
        [2, 3, 8, 0, 6, 5, 7, 8, 2, 3, 5, 4, 7, 1, 8, 8, 8, 3, 3, 7], 
        [7, 1, 6, 5, 0, 5, 6, 0, 5, 8, 3, 6, 2, 0, 2, 3, 2, 2, 1, 4], 
        [0, 5, 6, 3, 6, 0, 3, 0, 2, 6, 0, 3, 1, 3, 3, 7, 6, 0, 0, 5], 
        [2, 3, 4, 8, 6, 4, 0, 0, 7, 4, 2, 4, 0, 5, 5, 2, 7, 4, 2, 4], 
        [4, 7, 3, 4, 5, 6, 2, 0, 4, 1, 0, 0, 3, 5, 1, 4, 1, 5, 5, 4], 
        [8, 8, 0, 3, 7, 2, 7, 0, 0, 6, 1, 7, 0, 1, 4, 4, 3, 1, 4, 3], 
        [7, 4, 0, 4, 1, 7, 2, 6, 5, 0, 0, 3, 2, 5, 5, 8, 1, 6, 6, 5], 
        [0, 4, 6, 6, 6, 0, 2, 7, 8, 5, 0, 2, 1, 1, 1, 5, 0, 6, 6, 2], 
        [2, 5, 1, 4, 8, 0, 6, 7, 0, 1, 3, 0, 3, 6, 0, 3, 3, 4, 2, 6], 
        [1, 5, 3, 4, 0, 2, 4, 4, 4, 3, 5, 0, 0, 7, 4, 6, 1, 3, 5, 0], 
        [4, 1, 3, 1, 6, 6, 8, 3, 3, 4, 5, 1, 5, 0, 2, 7, 7, 2, 0, 2], 
        [7, 6, 3, 8, 1, 2, 5, 2, 3, 1, 2, 5, 5, 7, 0, 1, 4, 1, 0, 1], 
        [7, 8, 1, 0, 0, 6, 8, 7, 0, 7, 7, 0, 4, 3, 6, 0, 3, 4, 7, 3], 
        [3, 7, 2, 4, 3, 3, 4, 6, 7, 3, 0, 5, 3, 1, 8, 2, 0, 4, 6, 6], 
        [5, 4, 5, 8, 3, 5, 7, 1, 7, 1, 7, 2, 2, 3, 7, 7, 2, 0, 1, 0], 
        [1, 1, 7, 7, 2, 5, 0, 7, 3, 5, 7, 4, 4, 6, 5, 7, 8, 1, 0, 6], 
        [1, 6, 0, 5, 6, 8, 8, 2, 5, 7, 2, 8, 1, 7, 3, 0, 0, 5, 2, 0]
        ]
    N = [[j*PING_STANDARD_SIZE for j in i] for i in N]
    flow(G, N)
    capacity(G)
    title = "Choose option: "
    options = ["See Graph", "Test 1", "Test 2", "Test 3", "Exit"]
    exit = False
    while not exit:
        _option, index = pick(options, title, indicator='=>')
        match index:
            case 0:
                see_graph(G)
            case 1:
                t1(G, N)
            case 2:
                t2(G, N)
            case 3: 
                t3(G, N)
            case 4:
                exit = True
    

if __name__ == "__main__":
    main()