import networkx as nx
import Calc
import json

# TPN の隣接取得数により NDCG を比較. シートは NUM 毎に作成

EXCEL_NAME = "./実験結果.xlsx"
READ_SAMPLING_FILE = "./data/partition_data/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"
# 例               : "./data/partition_data/div_30/BFS/amazon0601/num_0/size_0.1/TPN/ver_0/synthesis.adjlist"
K_DIV = 0.01
DIV = 10

def excel_value(name, method, n_rate):
    if name == "p2p-Gnutella24":
        column = 2
    elif name == "scale_free":
        column = 3
    elif name == "wiki-Talk":
        column = 4
    elif name == "web-Google":
        column = 5
    elif name == "soc-Epinions1":
        column = 6
    elif name == "amazon0601":
        column = 7
    
    if method == "BFS":
        column += 8 * 0
    elif method == "NXMETIS":
        column += 8 * 1
    elif method == "BISECTION":
        column += 8 * 2
        
    if n_rate == 0:
        add = 0
    elif n_rate == 0.1:
        add = 1
    elif n_rate == 0.2:
        add = 2
    elif n_rate == 0.3:
        add = 3
    elif n_rate == 0.4:
        add = 4
    elif n_rate == 0.5:
        add = 5
    elif n_rate == 0.6:
        add = 6
    elif n_rate == 0.7:
        add = 7
    elif n_rate == 0.8:
        add = 8
    elif n_rate == 0.9:
        add = 9
    elif n_rate == 1:
        add = 10
    
    return column, add

def calc_cent(div, partition, graph, num, size, n_rate, k_div):
    sampling_graph = nx.read_adjlist(READ_SAMPLING_FILE.format(div, partition, graph, num, size, "TPN_{}".format(n_rate), 0), nodetype=int, create_using=nx.DiGraph)
    if graph == "web-Google":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_web_Google, k_div)
    elif graph == "amazon0601":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_amazon0601, k_div)
    elif graph == "p2p-Gnutella24":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_p2p_Gnutella24, k_div)
    elif graph == "soc-Epinions1":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_soc_Epinions1, k_div)
    elif graph == "scale_free":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_scale_free, k_div)
    elif graph == "wiki-Talk":
        ndcg = Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_wiki_Talk, k_div)

    column, add = excel_value(graph, partition, n_rate)
    row_ave = 2
    
    sheet_name = "TPN_neighbors_{}_true".format(num)
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=row_ave+add)

partition_list = ["BFS", "NXMETIS", "BISECTION"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2]
size_list = [0.1]
neighbor_rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

if "web-Google" in graph_list:
    with open('./data/partition_data/graph_cent/web-Google/pr.json', 'r') as f:
        pr_web_Google = json.load(f)
if "amazon0601" in graph_list:
    with open('./data/partition_data/graph_cent/amazon0601/pr.json', 'r') as f:
        pr_amazon0601 = json.load(f)
if "p2p-Gnutella24" in graph_list:
    with open('./data/partition_data/graph_cent/p2p-Gnutella24/pr.json', 'r') as f:
        pr_p2p_Gnutella24 = json.load(f)
if "soc-Epinions1" in graph_list:
    with open('./data/partition_data/graph_cent/soc-Epinions1/pr.json', 'r') as f:
        pr_soc_Epinions1 = json.load(f)
if "scale_free" in graph_list:
    with open('./data/partition_data/graph_cent/scale_free/pr.json', 'r') as f:
        pr_scale_free = json.load(f)
if "wiki-Talk" in graph_list:
    with open('./data/partition_data/graph_cent/wiki-Talk/pr.json', 'r') as f:
        pr_wiki_Talk = json.load(f)

for partition in partition_list:
    if partition == "NXMETIS":
        tmp_list = [0]
    else:
        tmp_list = num_list
    for graph in graph_list:
        for num in tmp_list:
            for size in size_list:
                for n_rate in neighbor_rate:
                    calc_cent(DIV, partition, graph, num, size, n_rate, K_DIV)