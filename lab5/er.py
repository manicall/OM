import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
from random import random, randint

def ER(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random()
        
        if a < p or combination[0] == 0:
            a, b = combination
            if a > b: a, b = b, a 
            E.add((a, b, randint(5,20)))
            
    return list(E)

if __name__ == "__main__":
    n = 10
    p = 0.35
    G = ER(n, p)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    plt.title("Random Graph Generation Example")
    plt.show()