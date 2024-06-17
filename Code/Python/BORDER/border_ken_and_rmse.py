import networkx as nx
import Calc
import Sampling as sp
import random
from scipy.stats import kendalltau
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

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
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.legend()
    plt.show()
    plt.close()

def make_plt_rmse(x_list_list, y_list_list, figsize=(6, 6), x_label=None, y_label=None, label_list=None, color_list=None, title=None, axis=["plain", "plain"], save_path=None):
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
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0)
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.legend()
    plt.show()
    plt.close()

def return_weight(origin_graph, connect_node_list, weight_range, default_weight):
    weight_dict = {node: default_weight for node in list(origin_graph)}
    for node in connect_node_list:
        weight_dict[node] = random.randint(default_weight+1, weight_range)
    
    return weight_dict

def return_sampling_graph(graph_name, graph, connect_node_list, sampling_rate, sampling_method, weight_dict, default_weight, weight_node_num, weight_range):
    sampling_graph = nx.DiGraph()
    if sampling_method == "RE":
        obj = sp.RE()
        sampling_graph = obj.random_edge_sampling(graph, sampling_rate)
    elif sampling_method == "FC":
        obj = sp.FC()
        sampling_graph = obj.flow_control_sampling(graph, sampling_rate, connect_node_list, weight_dict, default_weight)
    elif sampling_method == "FC_random":
        obj = sp.FC()
        sampling_graph = obj.fc_random_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_prefer_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_top_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_top_prefer_sampling(graph, sampling_rate, weight_node_num, default_weight, weight_range)
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
    
    return sampling_graph

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
    graph_name = "soc-Epinions1"
    # sampling_list = ["RE", "FC", "BC_in_out", "BC_in", "BC_out", "EBC"] # BC 系の比較
    # sampling_list = ["RE", "FC", "FC_random", "FC_prefer", "FC_top_prefer"] # FC 系の比較
    # sampling_list = ["RE", "FC", "CC_in_out", "CC_in", "CC_out"] # CC 系の比較
    sampling_list = ["FC", "EPR"] # PR 系の比較
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    border = "prefer"
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # rate_list = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    
    # 描画用パラメータ
    # color_list = ["olive", "orangered", "gold", "black", "blue", "red"] # BC & PR
    # color_list = ["olive", "orangered", "gold", "black", "blue"] # FC & CC
    color_list = ["red", "blue"]
    main_title = "ケンドールの順位相関係数_{}_重み個数{}_幅{}".format(border, weight_node_num, weight_range)
    x_label = "sampling size"
    y_label = "value"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    if border == "random":
        connect_node_list = Calc.select_border_node(origin_graph, weight_node_num) # ランダム選択
    elif border == "prefer":
        connect_node_list = Calc.select_border_prefer(origin_graph, weight_node_num) # 優先付着
    weight_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    
    x_list_list = [rate_list] * len(sampling_list)
    y_list_list = []
    for sampling in sampling_list:
        kendall_list = []
        for rate in rate_list:
            sampling_graph = return_sampling_graph(graph_name, origin_graph, connect_node_list, rate, sampling, weight_dict, default_weight, weight_node_num, weight_range)
            ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
            kendall_list.append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
        
        y_list_list.append(kendall_list)
    
    make_plt_ken(x_list_list, y_list_list, x_lim=rate_list[-1], x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list)

# FC と EPR の比較をちゃんとするために
def average_ken():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["FC", "EPR"] # PR 系の比較
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    sampling_num = 10
    border = "random"
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    # 描画用パラメータ
    color_list = ["red", "blue"]
    main_title = "ケンドールの順位相関係数_{}_重み個数{}_幅{}".format(border, weight_node_num, weight_range)
    x_label = "sampling size"
    y_label = "value"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    
    x_list_list = [rate_list] * len(sampling_list)
    y_list_list = []
    for sampling in sampling_list:
        kendall_list = [[] for _ in range(sampling_num)]
        for i in range(sampling_num):
            if border == "random":
                connect_node_list = Calc.select_border_node(origin_graph, weight_node_num) # ランダム選択
            elif border == "prefer":
                connect_node_list = Calc.select_border_prefer(origin_graph, weight_node_num) # 優先付着
            weight_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
            
            for j, rate in enumerate(rate_list):
                sampling_graph = nx.DiGraph()
                if sampling == "FC":
                    path = "../../../Sampling_Data/FC_{}/{}/ver_{}.adjlist".format(border, rate, i+1)
                    sampling_graph = Calc.read_graph(path)
                else:
                    sampling_graph = return_sampling_graph(graph_name, origin_graph, connect_node_list, rate, sampling, weight_dict, default_weight, weight_node_num, weight_range)
                ppr_sum_origin, ppr_sum_sampling = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict)
                kendall_list[j].append(Calc.calc_kendall(ppr_sum_origin, ppr_sum_sampling))
        for k in range(sampling_num):
            kendall_list[k] = sum(kendall_list[k]) / len(kendall_list[k])
        
        y_list_list.append(kendall_list)
    
    make_plt_ken(x_list_list, y_list_list, x_lim=rate_list[-1], x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list)

if __name__ == "__main__":
    main_ken()