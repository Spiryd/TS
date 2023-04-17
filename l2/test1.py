import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import linspace
from lista2 import test1, assign_capacity, assign_flow, T

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

assign_flow(G, N)
assign_capacity(G, N)

suma = sum(sum(r) for r in N)
min_Tmax = [T(G, suma, m) for m in range(1, 11)]

for m in range(4, 0, -2):
    startT = min_Tmax[m - 1]
    for p in [0.9, 0.95, 0.99]:
        plt.figure()
        plt.imshow(
            [
                test1(G, N, Tmax, p, m, step=100)
                for Tmax in linspace(startT, 10 * startT, num=10)
            ],
            extent=[0, 1000, startT, 10 * startT],
            aspect="auto",
            origin="lower",
            cmap=mpl.colormaps["plasma"]
        )
        plt.colorbar()
        plt.ylabel("T_max")
        plt.xlabel("Liczba dodanych pakietów przy p={}, m={}".format(p, m))
        plt.savefig("TEST1_{}_{}.png".format(m, p))
        plt.close()
