import Calc
import Sampling as sp
import networkx as nx
import time
import datetime

# サンプリングした合成グラフをディレクトリに保存

ORIGIN_FILE = "./data/partition_data/origin_graph/{}.adjlist"
SAVE_SYNTHESIS_FILE = "./data/partition_data/sampled/{}/{}/ver_{}/sampled.adjlist"

all_time_start = time.perf_counter()

def return_sampling_graph(origin_graph, graph_name, sampling_rate, sampling_name):
    print()
    print(graph_name, sampling_name, "RATE :", sampling_rate)
    
    sampling_size = int(len(list(origin_graph)) * sampling_rate)
    # RN
    if sampling_name == "RN":
        obj = sp.RN()
        sp_graph = obj.random_node_sampling(origin_graph, sampling_size)
    # RE
    elif sampling_name == "RE":
        obj = sp.RE()
        sp_graph = obj.random_edge_sampling(origin_graph, sampling_size)
    # FF
    elif sampling_name == "FF":
        obj = sp.FF()
        sp_graph = obj.forest_fire_sampling(origin_graph, sampling_size)
    # SRW
    elif sampling_name == "SRW":
        obj = sp.SRW()
        sp_graph = obj.simple_random_walk_sampling(origin_graph, sampling_size)
    # RPN
    elif sampling_name == "RPN":
        obj = sp.RPN()
        sp_graph = obj.random_pagerank_node_sampling(origin_graph, sampling_size)
    # RD
    elif sampling_name == "RD":
        obj = sp.RD(0.01, 0.1)
        sp_graph = obj.rank_degree_sampling(origin_graph, sampling_size)
    # TPN
    elif sampling_name == "TPN":
        obj = sp.TPN()
        sp_graph = obj.top_pagerank_sampling(origin_graph, sampling_size, 1)
    # TPN_re
    elif sampling_name == "TPN_re":
        obj = sp.TPN_re()
        sp_graph = obj.top_pagerank_sampling(origin_graph, sampling_size)
    elif sampling_name == "TP":
        obj = sp.TP()
        sp_graph = obj.top_pagerank_sampling(origin_graph, sampling_size)
    
    return sp_graph

graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
sampling_rate = [0.1]
# sampling_list = ["RN", "RE", "FF", "SRW", "RPN", "RD", "TPN"]
sampling_list = ["TP"]
ver_list = [0, 1, 2]

# サンプリンググラフのエッジ接続に利用するための元グラフ取得
origin_graph_list = []
for graph in graph_list:
    origin_graph = nx.read_adjlist(ORIGIN_FILE.format(graph), nodetype=int, create_using=nx.DiGraph)
    origin_graph_list.append(origin_graph)

for i, graph in enumerate(graph_list):
    for sampling in sampling_list:
        for ver in ver_list:
            for rate in sampling_rate:
                sampling_graph = return_sampling_graph(origin_graph_list[i], graph, rate, sampling)
                Calc.write_in_adjlist(sampling_graph, SAVE_SYNTHESIS_FILE.format(graph, sampling, ver))

all_time_end = time.perf_counter()
all_tim = all_time_end - all_time_start
print(datetime.timedelta(seconds=all_tim))