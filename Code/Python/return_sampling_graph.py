import Calc
import Sampling as sp
import networkx as nx
import time
import datetime

# サンプリングした合成グラフをディレクトリに保存

READ_TRUE_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/true_edge.adjlist"
READ_REP_FILE =  "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/cut_edge.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/origin/part_0.adjlist"
SAVE_SAMPLED_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/sampling/part_{}.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/size_0.1/FF/ver_0/sampling/part_0.adjlist"
SAVE_SYNTHESIS_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"

all_time_start = time.perf_counter()

'''
def return_sampling_graph(origin_graph, subgraph_list, repgraph_list, partition, graph_name, rate, sampling):
    sampled_subgraph_list = []
    
    rate = float(rate)
    print()
    print(partition, graph_name, sampling, "RATE :", rate)
    

    for i, subgraph in enumerate(subgraph_list):
        graph_size = int(len(list(subgraph)) * rate)
        if graph_size == 0:
            graph_size = 1
        
        # RE
        if sampling == "RE":
            obj = sp.RE()
            sp_graph = obj.random_edge_sampling(subgraph, graph_size)
        # FF
        elif sampling == "FF":
            obj = sp.FF()
            sp_graph = obj.forest_fire_sampling(subgraph, graph_size)
        # SRW
        elif sampling == "SRW":
            obj = sp.SRW()
            sp_graph = obj.simple_random_walk_sampling(subgraph, graph_size)
        # RPN
        elif sampling == "RPN":
            obj = sp.RPN()
            sp_graph = obj.random_pagerank_node_sampling(subgraph, graph_size)
        # RD
        elif sampling == "RD":
            obj = sp.RD(0.01, 0.1)
            sp_graph = obj.rank_degree_sampling(subgraph, graph_size)
        # TPN_re
        elif sampling == "TPN_re":
            obj = sp.TPN_re()
            acc = nx.average_clustering(subgraph)
            pr_origin = nx.pagerank(subgraph)
            sp_graph = obj.top_pagerank_sampling(subgraph, repgraph_list[i], acc, pr_origin)
        # TP_rep
        elif sampling == "TP_rep":
            obj = sp.TP_rep()
            sp_graph = obj.top_in_edge_sampling(subgraph, repgraph_list[i], graph_size)
        
        sampled_subgraph_list.append(sp_graph)
'''
    
    # グラフ内エッジの割合を基準に, それぞれからその割合分取得するという手法でとりあえず試してみる
def return_sampling_graph(origin_graph, subgraph_list, repgraph_list, partition, graph_name, sampling):
    sampled_subgraph_list = []

    print()
    print(partition, graph_name, sampling)
    intra_edge_num_list = []
    
    for subgraph in subgraph_list:
        intra_edge_num_list.append(len(list(subgraph.edges())))
    
    intra_sum = sum(intra_edge_num_list)
    
    for i in range(len(intra_edge_num_list)):
        intra_edge_num_list[i] /= intra_sum
    
    for i, subgraph in enumerate(subgraph_list):
        graph_size = int(len(list(subgraph)) * intra_edge_num_list[i])
        if graph_size == 0:
            graph_size = 1
        
        # RE
        if sampling == "RE":
            obj = sp.RE()
            sp_graph = obj.random_edge_sampling(subgraph, graph_size)
        # FF
        elif sampling == "FF":
            obj = sp.FF()
            sp_graph = obj.forest_fire_sampling(subgraph, graph_size)
        # SRW
        elif sampling == "SRW":
            obj = sp.SRW()
            sp_graph = obj.simple_random_walk_sampling(subgraph, graph_size)
        # RPN
        elif sampling == "RPN":
            obj = sp.RPN()
            sp_graph = obj.random_pagerank_node_sampling(subgraph, graph_size)
        # RD
        elif sampling == "RD":
            obj = sp.RD(0.01, 0.1)
            sp_graph = obj.rank_degree_sampling(subgraph, graph_size)
        # TPN_re
        elif sampling == "TPN_re":
            obj = sp.TPN_re()
            acc = nx.average_clustering(subgraph)
            pr_origin = nx.pagerank(subgraph)
            sp_graph = obj.top_pagerank_sampling(subgraph, graph_size, acc, pr_origin)
        # TP_rep
        elif sampling == "TP_rep":
            obj = sp.TP_rep()
            sp_graph = obj.top_in_edge_sampling(subgraph, repgraph_list[i], graph_size)
        
        sampled_subgraph_list.append(sp_graph)
    
    synthesis_graph = Calc.simple_graph_synthesis(origin_graph, sampled_subgraph_list)

    return sampled_subgraph_list, synthesis_graph

div_list = [10]
partition_list = ["RN", "BFS", "NXMETIS", "BISECTION"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0]
# sampling_rate = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08", "0.09", "0.10", "0.12", "0.14", "0.16", "0.18", "0.20", "0.22", "0.24", "0.26", "0.28", "0.30"]
sampling_rate = ["free"]
sampling_list = ["RE", "FF", "SRW", "RPN", "RD", "TPN_re", "TP_rep"]
ver_list = [0]

# サンプリンググラフのエッジ接続に利用するための元グラフ取得
origin_graph_list = []
for graph in graph_list:
    origin_graph = Calc.read_origin_graph(graph)
    origin_graph_list.append(origin_graph)

for div in div_list:
    for partition in partition_list:
        if partition == "NXMETIS":
            tmp_num = [0]
        else:
            tmp_num = num_list
        for l, graph in enumerate(graph_list):
            for num in tmp_num:
                subgraph_list = []
                repgraph_list = []
                for j in range(div):
                    subgraph = nx.read_adjlist(READ_TRUE_FILE.format(div, partition, graph, num, j), nodetype=int, create_using=nx.DiGraph)
                    repgraph = nx.read_adjlist(READ_REP_FILE.format(div, partition, graph, num, j), nodetype=int, create_using=nx.DiGraph)
                    subgraph_list.append(subgraph)
                    repgraph_list.append(repgraph)
                for rate in sampling_rate:
                    for sampling in sampling_list:
                        if sampling == "TPN_re" or "TP_rep":
                            tmp_ver = [0]
                        else:
                            tmp_ver = ver_list
                        for ver in tmp_ver:
                            sampled_subgraph_list, synthesis_graph = return_sampling_graph(origin_graph_list[l], subgraph_list, repgraph_list, partition, graph, sampling)
                            for m, subgraph in enumerate(sampled_subgraph_list):
                                Calc.write_in_adjlist(subgraph, SAVE_SAMPLED_FILE.format(div, partition, graph, num, rate, sampling, ver, m))
                            Calc.write_in_adjlist(synthesis_graph, SAVE_SYNTHESIS_FILE.format(div, partition, graph, num, rate, sampling, ver))

all_time_end = time.perf_counter()
all_tim = all_time_end - all_time_start
print(datetime.timedelta(seconds=all_tim))