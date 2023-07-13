import networkx as nx
import Calc
import json
from statistics import mean

# 手法毎の NDCG を比較. DIV 毎, NUM 毎にシートを作成

EXCEL_NAME = "./実験結果.xlsx"
READ_SAMPLING_FILE = "./data/partition_data/sampled/{}/{}/ver_{}/sampled.adjlist"
# 例 : "./data/partition_data/sampled/amazon0601/FF/ver_0/sampled.adjlist"
K_DIV = 0.01

def excel_value(name, sampling):
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
        
    if sampling == "RN":
        add = 0
    elif sampling == "RE":
        add = 1
    elif sampling == "FF":
        add = 2
    elif sampling == "SRW":
        add = 3
    elif sampling == "RPN":
        add = 4
    elif sampling == "RD":
        add = 5
    elif sampling == "TPN":
        add = 6
    elif sampling == "TPN_re":
        add = 7
    elif sampling == "TP":
        add = 8

    return column, add

def calc_cent(graph, sampling, ver_list, k_div):
    ndcg_pr_list = []
    
    for ver in ver_list:
        sampling_graph = nx.read_adjlist(READ_SAMPLING_FILE.format(graph, sampling, ver), nodetype=int, create_using=nx.DiGraph)
        ndcg_pr_list.append(Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_graph_dict[graph], k_div))
        
    column, add = excel_value(graph, sampling)
    row_ave = 2
    
    if len(ver_list) != 1:
        ndcg = mean(ndcg_pr_list)
    elif len(ver_list) == 1:
        ndcg = ndcg_pr_list[0]
    sheet_name = "NDCG_origin"
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=row_ave+add)

graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
# sampling_list = ["RN", "RE", "FF", "SRW", "RPN", "RD", "TPN"]
# ver_list = [0, 1, 2]
sampling_list = ["TP"]
ver_list = [0]

pr_graph_dict = {}
for name in graph_list:
    with open("./data/partition_data/graph_cent/{}/pr.json".format(name), "r") as f:
        pr_graph_dict[name] = json.load(f)

for graph in graph_list:
    for sampling in sampling_list:
        calc_cent(graph, sampling, ver_list, K_DIV)