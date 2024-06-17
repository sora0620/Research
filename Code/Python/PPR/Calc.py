import networkx as nx
import time
import numpy as np
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

# NDCG 2
#       exact : ranking & values  e.g., {"node1" : val1, "node2" : val2, ..., "nodek" : valk}
# approximate :          ranking  e.g., [node1, node2, ..., nodek]

# 自分がやっている研究に対しての利用方法
#       exact : 正解データとなる元グラフのノード番号と PR 値を格納した辞書
# approximate : 縮小グラフでのノードをランキングの昇順にリストに格納
# 実際に使う関数は calc_ndcg のみで良い

def dcg_2(approx_nodes, exact_dict, k): # べき乗型の DCG の計算
    approx_nodes = approx_nodes[:k]
    rtn = 0
    for i in range(k):
        rtn += ((2 ** exact_dict.get(approx_nodes[i], 0) - 1) / np.log2(i + 2))
    
    return rtn

def dcg_perfect_2(exact_dict, k): # DCG を正規化するために利用する理想的なランキング指標
    sorted_nodes = sorted(exact_dict.items(), key=lambda x: x[1], reverse=True)[:k]
    rtn = 0
    
    for i in range(len(sorted_nodes)):
        rtn += ((2 ** sorted_nodes[i][1] - 1) / np.log2(i + 2))
    
    return rtn

def calc_ndcg_2(approx_nodes, exact_dict, k): # DCG を正規化して NDCG を計算
    return dcg_2(approx_nodes, exact_dict, k) / dcg_perfect_2(exact_dict, k)

def calc_synthesis_pr_ndcg(sampled_graph, pr_origin, k_div):
        # sampled_graph : 縮小グラフ, nx.DiGraph 型
        #     pr_origin : 元グラフの PR, 辞書型, json で取得する場合はキーが str 型なので, 途中で int に変換して利用している
        #         k_div : NDCG の上位 k * 100 % の評価範囲を決める際の割合
        
        time_start = time.perf_counter()

        approximate = []
        exact = {}
        
        for k, v in pr_origin.items():
            if type(k) is str:
                exact[int(k)] = v
            else:
                exact[k] = v

        # 割合ではなく, 上位何ノードかを直接指定しちゃおう
        # sampled_graph_size = len(list(sampled_graph))
        # k_size = int(sampled_graph_size * k_div) # NDCG を計算する際の k 値
        k_size = k_div
        
        pr_sampled = nx.pagerank(sampled_graph)
        pr_sampled = sorted(pr_sampled.items(), key=lambda x:x[1], reverse=True)
        
        for node, pr in pr_sampled:
            approximate.append(node)
            
        time_end = time.perf_counter()
        tim = time_end - time_start
        print("Sampling PR Time :", tim)
            
        return calc_ndcg_2(approximate, exact, k_size)

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

def calc_rmse(origin_dict, sampling_dict):
    """
    RMSE を計算
    ただし, サンプリングしたノード数によって順位変動の大小に差が生じるのは当たり前なので, RMSE をノード数で割る.
    例えば, ノード数 10 の 1 位分の差は、ノード数 100 では 10 位分の差に該当する. これを同等と評価するには, ノード数で割ることで, 0.1 となる
    ↑ ちゃんとノード数で割っているのでこれ嘘だわw、もう削除しました

    Parameters:
        origin_dict, sampling_dict (dict): 辞書型の PR 結果等. ソート等をする必要は無し
    
    Return:
        RMSE
    """
    sampling_node_set = set(list(sampling_dict.keys()))
    
    num = len(sampling_node_set)
    sum = 0
    
    for node in sampling_node_set:
        sum += pow(origin_dict[node] - sampling_dict[node], 2)
    
    return math.sqrt(sum / num)

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
    with open(filename, 'w') as f:
        for node in list(G):
            f.write(f"{node}")
            f.write(" ")
            adj_node_list = list(G.successors(node))
            node_deg = len(adj_node_list)
            if node_deg != 0:
                for i, adj_node in enumerate(adj_node_list):
                    f.write(f"{adj_node}")
                    
                    if i != node_deg - 1:
                        f.write(" ")
            f.write("\n")