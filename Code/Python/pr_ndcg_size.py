import networkx as nx
import Calc
import json
from statistics import mean

# SAMPLING (基本的には TPN_re を想定) のサンプリング手法に関して, サンプリングサイズを変えた時の NDCG を, 各 num 毎にシートに記入
# 1 % ~ 10 % を想定

SAMPLING = "TPN_re"
EXCEL_NAME = "../../Excel/size.xlsx"
READ_SAMPLING_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"
# 例               : "../../Dataset/Partition/div_30/BFS/amazon0601/num_0/size_0.1/TPN/ver_0/synthesis.adjlist"
K_DIV = 0.01

def excel_value(name, method, size):
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
    
    if size == "0.01":
        add = 0
    elif size == "0.02":
        add = 1
    elif size == "0.03":
        add = 2
    elif size == "0.04":
        add = 3
    elif size == "0.05":
        add = 4
    elif size == "0.06":
        add = 5
    elif size == "0.07":
        add = 6
    elif size == "0.08":
        add = 7
    elif size == "0.09":
        add = 8
    elif size == "0.10":
        add = 9
    elif size == "0.12":
        add = 10
    elif size == "0.14":
        add = 11
    elif size == "0.16":
        add = 12
    elif size == "0.18":
        add = 13
    elif size == "0.20":
        add = 14
    elif size == "0.22":
        add = 15
    elif size == "0.24":
        add = 16
    elif size == "0.26":
        add = 17
    elif size == "0.28":
        add = 18
    elif size == "0.30":
        add = 19

    return column, add

def calc_cent(div, partition, graph, num, size, sampling, ver_list, k_div):
    ndcg_pr_list = []
    
    for ver in ver_list:
        sampling_graph = nx.read_adjlist(READ_SAMPLING_FILE.format(div, partition, graph, num, size, sampling, ver), nodetype=int, create_using=nx.DiGraph)
        ndcg_pr_list.append(Calc.calc_synthesis_pr_ndcg(sampling_graph, pr_graph_dict[graph], k_div))
    
    column, add = excel_value(graph, partition, size)
    row_ave = 2
    
    if len(ver_list) != 1:
        ndcg = mean(ndcg_pr_list)
    elif len(ver_list) == 1:
        ndcg = ndcg_pr_list[0]
    sheet_name = "num_{}".format(num)
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=row_ave+add)

div_list = [10]
partition_list = ["BFS", "BISECTION", "NXMEtIS"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
# num_list = [0, 1, 2]
num_list = [0]
# size_list = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08", "0.09", "0.10", "0.12", "0.14", "0.16", "0.18", "0.20", "0.22", "0.24", "0.26", "0.28", "0.30"]
size_list = ["0.10"]
if SAMPLING == "TPN_re":
    ver_list = [0]
else:
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
                    calc_cent(div, partition, graph, num, size, SAMPLING, ver_list, K_DIV)