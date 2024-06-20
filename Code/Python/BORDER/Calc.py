import networkx as nx
import random
import numpy as np
import json
from scipy.stats import kendalltau
import math

def read_graph(path):
    tmp_graph = nx.read_adjlist(path, nodetype=int, create_using=nx.DiGraph)
    print("Reading Completed!")
    
    return tmp_graph

def read_origin_graph(graph):
    file_name = "../../../Dataset/Origin/{}.adjlist"
    origin_graph = nx.read_adjlist(file_name.format(graph), nodetype=int, create_using=nx.DiGraph)
    
    print("Reading Completed! : {}".format(graph))
    
    return origin_graph

def select_border_node(graph, weight_node_num):
    return random.sample(list(graph.nodes()), weight_node_num)

# 優先付着ノード選択
def select_border_prefer(graph, weight_node_num):
    node_list = list(graph)
    deg_list = []
    
    sum = 0
    for node in node_list:
        deg = graph.in_degree(node)
        deg_list.append(deg)
        sum += deg
        
    for i in range(len(node_list)):
        deg_list[i] /= sum
    
    return np.random.choice(node_list, size=weight_node_num, p=deg_list, replace=False)

# 辞書型 (key: ノード, value: 値) の変数を, json に保存
def write_in_json(dic, path):
    with open(path, 'w') as f:
        json.dump(dic, f, indent=4, sort_keys=True)
    
    return

def calc_kendall(origin_dict, sampling_dict):
    """
    ケンドールの順位相関係数を計算

    Parameters:
        origin_dict, sampling_dict (dict): 辞書型の PR 結果等
    
    Return:
        ケンドールの順位相関係数
    """
    sampling_node_list = list(sampling_dict.keys())
    
    origin_list = []
    sampling_list = []
    
    for node in sampling_node_list:
        origin_list.append(origin_dict[node])
        sampling_list.append(sampling_dict[node])
    
    statistic, pvalue = kendalltau(origin_list, sampling_list)
    
    return statistic

def calc_rmse_top(origin_dict, sampling_dict, top_node_num):
    """
    RMSE を計算
    ただし, サンプリングしたノード数によって順位変動の大小に差が生じるのは当たり前なので, RMSE をノード数で割る.
    ノード数が多いと, 低ランクの誤差が少ないやつらに影響されて平均値が低くなってしまうので, 上位だけで比較したほうが適切かもしれない

    Parameters:
        origin_dict, sampling_dict (dict): 辞書型の PR 結果等. ソート等をする必要は無し
    
    Return:
        RMSE
    """
    origin_sorted = sorted(origin_dict.items(), key=lambda x: x[1], reverse=True)
    top_node_list = []
    sampling_node_set = set(list(sampling_dict.keys()))
    sum = 0
    
    for node, ppr in origin_sorted:
        if node in sampling_node_set:
            top_node_list.append(node)

    for node in top_node_list[:top_node_num]:
        sum += pow(origin_dict[node] - sampling_dict[node], 2)
    
    return math.sqrt(sum / top_node_num)

def write_in_adjlist(G, filename):
    f = open(filename, "w")
    node_list = list(G)
    
    for node in node_list:
        f.write(f"{node}")
        f.write(" ")
        adj_node_list = list(G.successors(node))
        node_deg = len(adj_node_list)
        for i, adj_node in enumerate(adj_node_list):
            f.write(f"{adj_node}")
            
            if i != node_deg - 1:
                f.write(" ")
        f.write("\n")
        
    f.close()

def read_connect_list(graph_name, type, weight_num, ver):
    path = "./connect_node/{}/{}/{}/ver_{}.txt".format(graph_name, type, weight_num, ver)
    return_list = []
    with open(path, 'r') as f:
        for l in f:
            return_list = list(map(int, l.split()))
    
    return return_list