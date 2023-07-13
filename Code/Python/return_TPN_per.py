import Calc
import Sampling as sp
import networkx as nx
import time
import datetime

# TPN の隣接取得割合を変えたサンプリンググラフをディレクトリに保存

EXCEL_NAME = "./実験結果.xlsx"
ORIGIN_FILE = "./data/partition_data/origin_graph/{}.adjlist"
READ_FILE = "./data/partition_data/div_{}/{}/{}/num_{}/origin/part_{}.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/origin/part_0.adjlist"
SAVE_SAMPLED_FILE = "./data/partition_data/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/sampling/part_{}.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/size_0.1/FF/ver_0/sampling/part_0.adjlist"
SAVE_SYNTHESIS_FILE = "./data/partition_data/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"

all_time_start = time.perf_counter()

def return_sampling_graph(origin_graph, subgraph_list, method, graph_name, sampling_rate, sampling_name, neighbor_rate):
    sampled_subgraph_list = []
    
    print()
    print(method, graph_name, sampling_name, "RATE :", sampling_rate, "N_PER : {}".format(neighbor_rate))
    
    for subgraph in subgraph_list:
        sampling_size = int(len(list(subgraph)) * sampling_rate)
        
        # TPN
        obj = sp.TPN()
        sp_graph = obj.top_pagerank_sampling(subgraph, sampling_size, neighbor_rate)

        sampled_subgraph_list.append(sp_graph)
        
    synthesis_graph = Calc.simple_graph_synthesis(origin_graph, sampled_subgraph_list)

    return sampled_subgraph_list, synthesis_graph

graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
sampling_rate = [0.1]
div_size = [10]
partition_list = ["RN", "BFS", "NXMETIS", "BISECTION"]
sampling_list = ["TPN"]
neighbor_rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
num_list = [0, 1, 2]
ver_list = [0]

# サンプリンググラフのエッジ接続に利用するための元グラフ取得
origin_graph_list = []
for graph in graph_list:
    origin_graph = web_Google = nx.read_adjlist(ORIGIN_FILE.format(graph), nodetype=int, create_using=nx.DiGraph)
    origin_graph_list.append(origin_graph)

for div in div_size:
    for partition in partition_list:
        if partition == "NXMETIS":
            tmp_num = [0]
        else:
            tmp_num = num_list
        for l, graph in enumerate(graph_list):
            for num in tmp_num:
                subgraph_list = []
                for j in range(div):
                    subgraph = nx.read_adjlist(READ_FILE.format(div, partition, graph, num, j), nodetype=int, create_using=nx.DiGraph)
                    subgraph_list.append(subgraph)
                for rate in sampling_rate:
                    for sampling in sampling_list:
                        for n_rate in neighbor_rate:
                            for ver in ver_list:
                                sampled_subgraph_list, synthesis_graph = return_sampling_graph(origin_graph_list[l], subgraph_list, partition, graph, rate, sampling, n_rate)
                                for m, subgraph in enumerate(sampled_subgraph_list):
                                    Calc.write_in_adjlist(subgraph, SAVE_SAMPLED_FILE.format(div, partition, graph, num, rate, "TPN_{}".format(n_rate), ver, m))
                                Calc.write_in_adjlist(synthesis_graph, SAVE_SYNTHESIS_FILE.format(div, partition, graph, num, rate, "TPN_{}".format(n_rate), ver))

all_time_end = time.perf_counter()
all_tim = all_time_end - all_time_start
print(datetime.timedelta(seconds=all_tim))