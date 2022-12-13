import networkx as nx
import matplotlib.pyplot as plt

from kruskal import Kruskal
from er import ER

G = nx.Graph() 

E = None
if E is None:
    n = 7
    p = 0.5
    E = ER(n, p)

G.add_weighted_edges_from(E)
for e1, e2 in G.edges(): G[e1][e2]['color'] = 'black'
pos=nx.circular_layout(G)

g = Kruskal(E)
res = g.kruskal()
print(res)

for r1, r2, w in res:
    for e1, e2 in G.edges():
        if r1 == e1 and r2 == e2 or r1 == e2 and r2 == e1:
            G[e1][e2]['color'] = 'red'
            colors = nx.get_edge_attributes(G,'color').values()
            
            nx.draw(G, pos, edge_color=colors, with_labels=True, font_weight='bold',)
            edge_weight = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)

            plt.show()
            break
