import networkx as nx
import Calc
import json

# TPN の隣接取得数により NDCG を比較. シートは NUM 毎に作成

EXCEL_NAME = "./実験結果.xlsx"
READ_SAMPLING_FILE = "./data/partition_data/sampled/{}/TPN_{}/ver_{}/sampled.adjlist"
K_DIV = 0.01

def excel_value(name, n_rate):
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

def calc_cent(graph, n_rate, k_div):
    sampling_graph = nx.read_adjlist(READ_SAMPLING_FILE.format(graph, n_rate, 0), nodetype=int, create_using=nx.DiGraph)
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
        
    column, add = excel_value(graph, n_rate)
    row_ave = 2
    
    sheet_name = "TPN_origin"
    Calc.write_excel(ndcg, EXCEL_NAME, sheet_name, column=column, row=row_ave+add)

graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
sampling_list = ["TPN_{}"]
neighbor_rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

if "web-Google" in graph_list:
    with open('../Dataset/Origin/Centrality/web-Google/pr.json', 'r') as f:
        pr_web_Google = json.load(f)
if "amazon0601" in graph_list:
    with open('../Dataset/Origin/Centrality/amazon0601/pr.json', 'r') as f:
        pr_amazon0601 = json.load(f)
if "p2p-Gnutella24" in graph_list:
    with open('../Dataset/Origin/Centrality/p2p-Gnutella24/pr.json', 'r') as f:
        pr_p2p_Gnutella24 = json.load(f)
if "soc-Epinions1" in graph_list:
    with open('../Dataset/Origin/Centrality/soc-Epinions1/pr.json', 'r') as f:
        pr_soc_Epinions1 = json.load(f)
if "scale_free" in graph_list:
    with open('../Dataset/Origin/Centrality/scale_free/pr.json', 'r') as f:
        pr_scale_free = json.load(f)
if "wiki-Talk" in graph_list:
    with open('../Dataset/Origin/Centrality/wiki-Talk/pr.json', 'r') as f:
        pr_wiki_Talk = json.load(f)

for graph in graph_list:
    for n_rate in neighbor_rate:
        calc_cent(graph, n_rate, K_DIV)