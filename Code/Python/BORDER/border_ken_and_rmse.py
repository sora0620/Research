import networkx as nx
import Calc
import Sampling as sp
import random
from scipy.stats import kendalltau
import json
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

ALPHA = 0.15

def make_plt_ken(x_list_list, y_list_list, figsize=(6, 6), x_lim=None, x_label=None, y_label=None, label_list=None, color_list=None, title=None, axis=["plain", "plain"], save_path=None):
    """
    １つのグラフを表示するための関数

    Parameters:
        x_list, y_list (list): 表示したいデータ群
        figsize (taple): グラフ全体のサイズ
        graph_label (string): グラフの凡例 (名前表示)
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
        title (string): グラフのタイトル
        axis (string): 軸の表記を設定. "plain" はそのまま, "sci" を指定すると指数表記になる. なお, [x 軸, y 軸] で指定
        save_path (string): .pngとして保存したい場合, パスを指定
    """
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    for i in range(len(x_list_list)):
        ax.plot(x_list_list[i], y_list_list[i], label=label_list[i], c=color_list[i], marker="o")
    
    # ax の設定
    if title != None:
        ax.set_title(title)
    if x_label != None:
        ax.set_xlabel(x_label)
    if y_label != None:
        ax.set_ylabel(y_label)
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style=axis[0], axis="x", scilimits=(0,0))
    ax.ticklabel_format(style=axis[1], axis="y", scilimits=(0,0))
    if x_lim == 1:
        ax.set_xlim(left=0, right=1)
    elif x_lim == 0.1:
        ax.set_xlim(left=0, right=0.1)
    ax.set_ylim(bottom=0, top=1)
    
    plt.tight_layout()
    plt.legend()
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    plt.close()

def return_weight(connect_node_list, weight_range, default_weight):
    weight_dict = {}
    for node in connect_node_list:
        weight_dict[node] = random.randint(default_weight+1, weight_range) - default_weight
    
    print("境界ノードの重み計算完了")
    return weight_dict

def read_ppr(path):
    ppr_dict = {}
    return_dict = {}
    
    with open(path, 'r') as f:
        ppr_dict = json.load(f)
    
    for key, value in ppr_dict.items():
        return_dict[int(key)] = value
    
    return return_dict

def return_ppr_dict(graph_name, connect_node_list):
    return_dict = {}
    
    for node in connect_node_list:
        path = "../../../Dataset/Centrality/PPR/{}/{}.json".format(graph_name, node)
        ppr_dict = read_ppr(path)
        return_dict[node] = ppr_dict
    
    print("PPR の読み込み完了")
        
    return return_dict

def return_edge_weight(graph, connect_node_list, weight_dict, ppr_dict):
    edge_list = list(graph.edges())
    edge_weight = {}
    for edge in edge_list:
        edge_weight[edge] = 0
        for node in connect_node_list:
            edge_weight[edge] += ppr_dict[node][edge[0]] * ((1 - ALPHA) / ALPHA) / graph.out_degree(edge[0]) * weight_dict[node]
    
    edge_weight_sorted = sorted(edge_weight.items(), key=lambda x: x[1], reverse=True)
    
    print("エッジの重み計算完了")
    
    return edge_weight_sorted

def return_sampling_graph(graph_name, graph, sampling_rate, sampling_method, connect_node_list):
    weight_node_num = len(connect_node_list)
    sampling_graph = nx.DiGraph()
    if sampling_method == "RE":
        obj = sp.RE()
        sampling_graph = obj.random_edge_sampling(graph, sampling_rate)
    elif sampling_method == "FC_random":
        obj = sp.FC()
        sampling_graph = obj.fc_random_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_prefer_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_top_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_top_prefer_sampling(graph, sampling_rate, weight_node_num)
    elif sampling_method == "BC_in_out":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_in_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "BC_in":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_in_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "BC_out":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "EBC":
        obj = sp.EBC()
        sampling_graph = obj.edge_betweenness_centraliry_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_in_out":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_in_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_in":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_in_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_out":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "PR_in_out":
        obj = sp.PR()
        sampling_graph = obj.pagerank_in_out_sampling(graph, sampling_rate)
    elif sampling_method == "PR_in":
        obj = sp.PR()
        sampling_graph = obj.pagerank_in_sampling(graph, sampling_rate)
    elif sampling_method == "PR_out":
        obj = sp.PR()
        sampling_graph = obj.pagerank_out_sampling(graph, sampling_rate)
    elif sampling_method == "EPR":
        obj = sp.EPR()
        sampling_graph = obj.edge_pagerank_sampling(graph, sampling_rate)
    else:
        print("Sampling Error!")
        exit(1)
    
    # 境界ノードとその周辺の出エッジが取得されないと困るので、取得されていない場合は必ずサンプリング割合分だけ取得されるように設定
    for node in connect_node_list:
        if node not in set(list(sampling_graph)):
            sampling_graph.add_node(node)
        out_edge_list = list(graph.successors(node))
        if sampling_graph.out_degree(node) == 0 and len(out_edge_list) != 0:            
            get_out_num = int(len(out_edge_list) * sampling_rate)
            if get_out_num == 0:
                get_out_num = 1
            
            tmp_list = random.sample(out_edge_list, get_out_num)
            for out_node in tmp_list:
                sampling_graph.add_edge(node, out_node)
    
    print("Sampling_Graph: ", sampling_graph)
    
    return sampling_graph

def return_rate_sampling_graph(graph, sampling_method, connect_node_list, sampling_rate_list, edge_weight_sorted):
    sampling_graph_list = []
    if sampling_method == "FC":
        obj = sp.FC()
        sampling_graph_list = obj.read_rate_flow_control_sampling(graph, sampling_rate_list, edge_weight_sorted)
    else:
        print("Sampling Error!")
        exit(1)
    
    for i, sampling_graph in enumerate(sampling_graph_list):
        for node in connect_node_list:
            if node not in set(list(sampling_graph)):
                sampling_graph.add_node(node)
            out_edge_list = list(graph.successors(node))
            if sampling_graph.out_degree(node) == 0 and len(out_edge_list) != 0:
                get_out_num = int(len(out_edge_list) * sampling_rate_list[i])
                if get_out_num == 0:
                    get_out_num = 1
                
                tmp_list = random.sample(out_edge_list, get_out_num)
                for out_node in tmp_list:
                    sampling_graph.add_edge(node, out_node)
        print("Sampling_Graph: ", sampling_graph)
    
    return sampling_graph_list

def return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict):
    personalization_origin = {node: 0 for node in list(origin_graph)}
    personalization_sampling = {node: 0 for node in list(sampling_graph)}
    
    for node in connect_node_list:
        personalization_origin[node] = weight_dict[node]
        personalization_sampling[node] = weight_dict[node]
    
    ppr_sum_origin = nx.pagerank(origin_graph, personalization=personalization_origin)
    ppr_sum_sampling = nx.pagerank(sampling_graph, personalization=personalization_sampling)
    
    return ppr_sum_origin, ppr_sum_sampling

def main_ken():
    # ハイパーパラメータ
    graph_name = "twitter"
    # sampling_list = ["RE", "FC", "BC_in_out", "BC_in", "BC_out", "EBC"] # BC 系の比較
    # sampling_list = ["RE", "FC", "FC_random", "FC_prefer", "FC_top_prefer"] # FC 系の比較
    # sampling_list = ["RE", "FC", "CC_in_out", "CC_in", "CC_out"] # CC 系の比較
    # sampling_list = ["FC", "EPR", "PR_out"] # PR 系の比較
    sampling_list = ["PR_out"]
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    border = "prefer"
    border_ver = 1
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # rate_list = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    save_file = "../pic/result.png"
    
    # 描画用パラメータ
    # color_list = ["olive", "orangered", "gold", "black", "blue", "red"] # BC & PR
    # color_list = ["olive", "orangered", "gold", "black", "blue"] # FC & CC
    # color_list = ["red", "blue", "green"]
    color_list = ["red", "blue"]
    main_title = "ケンドールの順位相関係数_{}_重み個数{}_幅{}".format(border, weight_node_num, weight_range)
    x_label = "sampling size"
    y_label = "value"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    connect_node_list = Calc.read_connect_list(graph_name, border, weight_node_num, border_ver)
    ppr_dict = return_ppr_dict(graph_name, connect_node_list)
    weight_dict = return_weight(connect_node_list, weight_range, default_weight)
    
    x_list_list = [rate_list] * len(sampling_list)
    y_list_list = []
    for sampling in sampling_list:
        kendall_list = []
        if sampling == "FC":
            edge_weight_sorted = return_edge_weight(origin_graph, connect_node_list, weight_dict, ppr_dict)
            sampling_graph_list = return_rate_sampling_graph(origin_graph, sampling, connect_node_list, rate_list, edge_weight_sorted)
            for sampling_graph in sampling_graph_list:
                ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
                kendall_list.append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
        else:
            for rate in rate_list:
                # FC でパス読み取る用 -> C++ の結果が正しいかの確認用
                # path = "../../../Dataset/FC/{}/境界ノード_{}/{}/ver_{}.adjlist".format(graph_name, weight_node_num, rate, 1)
                # sampling_graph = Calc.read_graph(path)
                
                # # 普通にサンプリング
                sampling_graph = return_sampling_graph(graph_name, origin_graph, rate, sampling, connect_node_list)
                ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
                kendall_list.append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
        
        y_list_list.append(kendall_list)
    
    make_plt_ken(x_list_list, y_list_list, x_lim=rate_list[-1], x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list, save_path=save_file)

# FC と EPR の比較をちゃんとするために
def average_ken():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["FC", "EPR", "PR_out"] # PR 系の比較
    weight_node_num = 100 # 境界ノードの数
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    sampling_num = 3 # 何回の平均を取るか, 今 PPR は 3 回分しかないので 3 回にしよう
    border = "prefer"
    # rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # rate_list = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    rate_list = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]
    color_list = ["red", "blue", "green"]
    
    # 描画用パラメータ
    main_title = "{}_個数{}".format(border, weight_node_num, weight_range)
    x_label = "sampling size"
    y_label = "value"
    save_file = f"../../../Picture/Border/{graph_name}/境界_{weight_node_num}_{rate_list[-1]}.png"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    
    x_list_list = [rate_list] * len(sampling_list)
    y_list_list = []
    for sampling in sampling_list:
        kendall_list = [[] for _ in range(len(rate_list))]
        for i in range(sampling_num):
            connect_node_list = Calc.read_connect_list(graph_name, border, weight_node_num, i)
            ppr_dict = return_ppr_dict(graph_name, connect_node_list)
            weight_dict = return_weight(connect_node_list, weight_range, default_weight)
            
            if sampling == "FC":
                edge_weight_sorted = return_edge_weight(origin_graph, connect_node_list, weight_dict, ppr_dict)
                sampling_graph_list = return_rate_sampling_graph(origin_graph, sampling, connect_node_list, rate_list, edge_weight_sorted)
                for j, sampling_graph in enumerate(sampling_graph_list):
                    ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
                    kendall_list[j].append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
            else:
                for j, rate in enumerate(rate_list):
                    sampling_graph = return_sampling_graph(graph_name, origin_graph, rate, sampling, connect_node_list)
                    ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
                    kendall_list[j].append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
        for k in range(len(rate_list)):
            kendall_list[k] = sum(kendall_list[k]) / len(kendall_list[k])
        
        y_list_list.append(kendall_list)
    
    make_plt_ken(x_list_list, y_list_list, x_lim=rate_list[-1], x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list, save_path=save_file)

if __name__ == "__main__":
    average_ken()
    # main_ken()