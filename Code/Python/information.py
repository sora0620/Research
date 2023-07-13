import networkx as nx
import os
import copy
import Calc

DIR = "./data/partition_data/origin_graph" # ディレクトリを選択, ここのみ変更
INFORMATION_FILE = DIR + "/information.txt"

graph_list = os.listdir(DIR)
if "information.txt" in graph_list:
    graph_list.remove("information.txt")
if "notice.txt" in graph_list:
    graph_list.remove("notice.txt")

graph_name = copy.deepcopy(graph_list)
for i, graph in enumerate(graph_list):
    graph_list[i] = DIR + "/{}".format(graph)

f = open(INFORMATION_FILE, "w")

for i, graph in enumerate(graph_list):
    print(graph)
    G = nx.read_adjlist(graph, nodetype=int, create_using=nx.DiGraph)
    coefficient = Calc.calc_clustering(G)
    f.write("{}, node : {}, edge : {}, clustering : {}\n".format(graph_name[i], len(list(G)), len(list(G.edges())), coefficient))
    
f.close()