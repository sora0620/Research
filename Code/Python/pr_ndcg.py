import networkx as nx
import Calc
import json
from statistics import mean

# 手法毎の NDCG を比較. DIV 毎, NUM 毎にシートを作成

EXCEL_NAME = "../../Excel/実験結果.xlsx"
K_DIV = 0.01

def excel_value(name, method, sampling):
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
        
    if sampling == "RE":
        add = 0
    elif sampling == "FF":
        add = 1
    elif sampling == "SRW":
        add = 2
    elif sampling == "RPN":
        add = 3
    elif sampling == "RD":
        add = 4
    elif sampling == "TPN_re":
        add = 5
    elif sampling == "TP_rep":
        add = 6

    return column, add

def calc_cent(div, partition, graph, num, size, sampling, ver_list, k_div):
    ndcg_pr_list = []
    
    if sampling == "TPN_re" or "TP_rep":
        ver_list = [0]
    
    for ver in ver_list:
        sampling_graph = Calc.read_sampling_graph(div, partition, graph, num, size, sampling, ver)
        ndcg_pr_list.append(Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_graph_dict[graph], k_div))
        
    column, add = excel_value(graph, partition, sampling)
    row_ave = 2
    
    if len(ver_list) != 1:
        ndcg = mean(ndcg_pr_list)
    elif len(ver_list) == 1:
        ndcg = ndcg_pr_list[0]
    sheet_name = "NDCG_{}_{}_true".format(div, num)
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=row_ave+add)

div_list = [10]
partition_list = ["BFS", "NXMETIS", "BISECTION"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2]
size_list = ["0.10"]
sampling_list = ["FF", "RD", "RE", "RPN", "SRW", "TP_rep", "TPN_re"]
ver_list = [0, 1, 2]

pr_graph_dict = {}
for name in graph_list:
    with open("../../Dataset/Origin/Centrality/{}/pr.json".format(name), "r") as f:
        pr_graph_dict[name] = json.load(f)

for div in div_list:
    for partition in partition_list:
        if partition == "NXMETIS":
            tmp_list = [0]
        else:
            tmp_list = num_list
        for graph in graph_list:
            for num in tmp_list:
                for size in size_list:
                    for sampling in sampling_list:
                        calc_cent(div, partition, graph, num, size, sampling, ver_list, K_DIV)