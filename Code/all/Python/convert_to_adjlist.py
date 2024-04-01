import networkx as nx
import Calc

# ./graph に保存される. その後グラフサイズが大きければ縮小し, ./data/partition_data/origin_graph にコピペで移せば OK

SAVE_FILE = "../../Dataset/Origin/{}.adjlist"

GRAPH_NAME = "com3" # ここを変更

PATH = "../../Dataset/Origin/{}.txt".format(GRAPH_NAME)

G = nx.read_edgelist(PATH, nodetype=int, create_using=nx.DiGraph)
Calc.write_in_adjlist(G, SAVE_FILE.format(GRAPH_NAME))