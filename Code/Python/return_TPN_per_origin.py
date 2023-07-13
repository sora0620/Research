import Calc
import Sampling as sp
import networkx as nx
import time
import datetime

# サンプリングした合成グラフをディレクトリに保存

ORIGIN_FILE = "./data/partition_data/origin_graph/{}.adjlist"
SAVE_SYNTHESIS_FILE = "./data/partition_data/sampled/{}/TPN_{}/ver_{}/sampled.adjlist"

all_time_start = time.perf_counter()

def return_sampling_graph(origin_graph, graph_name, sampling_rate, sampling_name, n_rate):
    print()
    print(graph_name, sampling_name, "RATE :", n_rate)
    
    sampling_size = int(len(list(origin_graph)) * sampling_rate)
    # TPN
    obj = sp.TPN()
    sp_graph = obj.top_pagerank_sampling(origin_graph, sampling_size, n_rate)
    
    return sp_graph

graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
sampling_rate = [0.1]
sampling_list = ["TPN"]
ver_list = [0]
neighbor_rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

# サンプリンググラフのエッジ接続に利用するための元グラフ取得
origin_graph_list = []
for graph in graph_list:
    origin_graph = nx.read_adjlist(ORIGIN_FILE.format(graph), nodetype=int, create_using=nx.DiGraph)
    origin_graph_list.append(origin_graph)

for i, graph in enumerate(graph_list):
    for sampling in sampling_list:
        for n_rate in neighbor_rate:
            for ver in ver_list:
                for rate in sampling_rate:
                    sampling_graph = return_sampling_graph(origin_graph_list[i], graph, rate, sampling, n_rate)
                    Calc.write_in_adjlist(sampling_graph, SAVE_SYNTHESIS_FILE.format(graph, n_rate, ver))

all_time_end = time.perf_counter()
all_tim = all_time_end - all_time_start
print(datetime.timedelta(seconds=all_tim))