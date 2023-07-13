import networkx as nx
import json
import Calc

K_DIV = 0.01
EXCEL_NAME = "../../Excel/元グラフの上位 0.1 % がサンプリンググラフに含まれる割合.xlsx"
ROW = 2
ORIGIN_FILE = "../../Dataset/Origin/Centrality/{}/pr.json"
SAMPLING_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_0.10/TPN_re/ver_0/synthesis.adjlist"

def excel_value(graph, partition):
    if graph == "p2p-Gnutella24":
        column = 2
    elif graph == "scale_free":
        column = 3
    elif graph == "wiki-Talk":
        column = 4
    elif graph == "web-Google":
        column = 5
    elif graph == "soc-Epinions1":
        column = 6
    elif graph == "amazon0601":
        column = 7
    
    if partition == "BFS":
        column += 8 * 0
    elif partition == "NXMETIS":
        column += 8 * 1
    elif partition == "BISECTION":
        column += 8 * 2
    elif partition == "RN":
        column += 8 * 3

    return column

# NDCG と、それに対して元グラフの上位 0.1 % のノードがどれくらいの割合サンプリンググラフに含まれているかをエクセルに示す

def return_ratio(origin_pr, sampling_graph):
    sampling_node_set = set(list(sampling_graph))

    sampling_node_num = sampling_graph.number_of_nodes()
    sampling_pr = nx.pagerank(sampling_graph)
    sorted_sampling_pr = sorted(sampling_pr.items(), key=lambda x:x[1], reverse=True)

    sorted_origin_pr = sorted(origin_pr.items(), key=lambda x:x[1], reverse=True)
    origin_top_nodes_set = set()

    i = 0
    relative_node_num = int(sampling_node_num * K_DIV)

    for key, value in sorted_origin_pr:
        if i >= relative_node_num:
            break
        
        origin_top_nodes_set.add(key)
        i += 1

    origin_in_sun = 0
    top_pr_in = 0
    
    tmp_set = set()
    
    for taple in sorted_sampling_pr[:relative_node_num]:
        tmp_set.add(taple[0])
    
    for node in origin_top_nodes_set:
        if node in sampling_node_set:
            origin_in_sun += 1
            if node in tmp_set:
                top_pr_in += 1

    return origin_in_sun / len(origin_top_nodes_set), top_pr_in / origin_in_sun

def main_fact(div, partition, graph, num):
    with open(ORIGIN_FILE.format(graph), "r") as file:
        json_pr = json.load(file)
        
    origin_pr = {}
    
    for k, v in json_pr.items():
        origin_pr[int(k)] = v
        
    sampling_graph = nx.read_adjlist(SAMPLING_FILE.format(div, partition, graph, num), nodetype=int, create_using=nx.DiGraph)
    
    ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, origin_pr, K_DIV)
    origin_in_ratio, top_in_ratio = return_ratio(origin_pr, sampling_graph)
    
    column = excel_value(graph, partition)
    
    sheet_name = "div_{}, num_{}".format(div, num)
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=ROW)
    Calc.write_excel(origin_in_ratio, EXCEL_NAME, sheet_name, column=column, row=ROW+1)
    Calc.write_excel(top_in_ratio, EXCEL_NAME, sheet_name, column=column, row=ROW+2)

div_list = [2, 10]
# partition_list = ["BFS", "NXMETIS", "BISECTION"]
partition_list = ["RN"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2]

for div in div_list:
    for partition in partition_list:
        for graph in graph_list:
            if partition == "NXMETIS":
                tmp_num = [0]
            else:
                tmp_num = num_list
            for num in tmp_num:
                main_fact(div, partition, graph, num)