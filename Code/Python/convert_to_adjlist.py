import networkx as nx
import Calc

# ./graph に保存される. その後グラフサイズが大きければ縮小し, ./data/partition_data/origin_graph にコピペで移せば OK

SAVE_FILE = "./graph/{}.adjlist"

# 以下を変更
GRAPH = "./data/solo_data/wiki-Vote.txt" # グラフの相対パス
SAVE_NAME = "wiki-Vote" # グラフの保存名

G = nx.read_edgelist(GRAPH, nodetype=int, create_using=nx.DiGraph)
Calc.write_in_adjlist(G, SAVE_FILE.format(SAVE_NAME))