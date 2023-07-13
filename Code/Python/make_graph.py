import networkx as nx
import Calc

# グラフの構築
G = nx.scale_free_graph(50000, alpha=0.4, beta=0.57, gamma=0.03)

print(G)
Calc.write_in_adjlist(G, "./data/partition_data/origin_graph/scale_free_2.adjlist")