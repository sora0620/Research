import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np

# ランキングの散布図を表示

EXCEL_NAME = "./実験結果.xlsx"
READ_SAMPLING_FILE = "./data/partition_data/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"
# 例               : "./data/partition_data/div_30/BFS/amazon0601/num_0/size_0.1/TPN/ver_0/synthesis.adjlist"
K_DIV = 0.01

def rank_return(div, partition, graph, num, size, sampling, ver, k_div):
    synthesis_graph = nx.read_adjlist(READ_SAMPLING_FILE.format(div, partition, graph, num, size, sampling, ver), nodetype=int, create_using=nx.DiGraph)
    exact = {}
    pr_origin = pr_graph_list[graph]

    sampled_graph_size = len(list(synthesis_graph))
    k_size = int(sampled_graph_size * k_div) # NDCG を計算する際の k 値
    pr_sampled = nx.pagerank(synthesis_graph)
    pr_sampled = sorted(pr_sampled.items(), key=lambda x:x[1], reverse=True)
    pr_sampled = pr_sampled[:k_size]
    
    for node, pr in pr_origin.items():
        exact[int(node)] = pr
        
    exact = sorted(exact.items(), key=lambda x:x[1], reverse=True)

    # {ノード番号 : 順位} の dict 型
    origin_node_ranking = {}
    for i, taple in enumerate(exact):
        origin_node_ranking[taple[0]] = i + 1
    
    node_ranking = {} # {ノード番号 : [縮小グラフの順位, 元グラフの順位]}
    for i, taple in enumerate(pr_sampled):
        node_ranking[taple[0]] = [i + 1, origin_node_ranking[taple[0]]]
    
    x_list = []
    y_list = []
    
    for v in node_ranking.values():
        x_list.append(v[1])
        y_list.append(v[0])
    
    return x_list, y_list

div_list = [10]
size_list = [0.1]
ver_list = [0]

# ndcg = 0.99
# partition = "NXMETIS"
# graph = "scale_free"
# sampling = "TPN"
# num = 0

# ndcg = 0.95
# partition = "NXMETIS"
# graph = "amazon0601"
# sampling = "TPN"
# num = 0

# ndcg = 0.90
# partition = "BISECTION"
# graph = "wiki-Talk"
# sampling = "TPN"
# num = 1

# ndcg = 0.85
# partition = "BFS"
# graph = "p2p-Gnutella24"
# sampling = "TPN"
# num = 2

ndcg = 0.81
partition = "NXMETIS"
graph = "p2p-Gnutella24"
sampling = "TPN"
num = 0

pr_graph_list = {}
with open("./data/partition_data/graph_cent/{}/pr.json".format(graph), "r") as f:
    pr_graph_list[graph] = json.load(f)

for div in div_list:
    for size in size_list:
        for ver in ver_list:
            x_list, y_list = rank_return(div, partition, graph, num, size, sampling, ver, K_DIV)

fig, ax = plt.subplots()

ax.set_xlabel("Origin Rank")
ax.set_ylabel("Sampled Rank")
ax.set_yscale("linear")
ax.set_aspect("equal")
ax.set_title("{}\n{}\nNDCG = {:.2f}".format(partition, graph, ndcg))

x_max = max(y_list)
y_max = max(x_list)
if x_max > y_max:
    m = x_max
else:
    m = y_max
m = 300
ax.set_xlim(right=m)
ax.set_ylim(top=m)
ax.scatter(x_list, y_list, s=5, color="red", label="{}".format(sampling))

x = np.arange(0, m+1)
y = x
plt.plot(x, y)

ax.legend(loc=0)

plt.show()