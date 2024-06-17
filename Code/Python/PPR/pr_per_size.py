import networkx as nx
import Calc
import Sampling as sp
import random
from scipy.stats import kendalltau
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

# y 軸の描画範囲が異なるだけ
def make_plt_ken(x_list_list, y_list_list, figsize=(6, 6), x_label=None, y_label=None, label_list=None, color_list=None, title=None, axis=["plain", "plain"], save_path=None):
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
    personalization_dict = {node: default_weight for node in list(origin_graph)}
    for node in connect_node_list:
        personalization_dict[node] = random.randint(default_weight+1, weight_range)
    
    return personalization_dict

def return_ppr_dict(origin_graph, connect_node_list):
    print("FC の PPR 計算開始")
    
    node_list = list(origin_graph)
    
    # 任意の１ノードを起点とした PPR 辞書を取得
    def get_ppr(source_node):
        ppr_weight = {node: 0 for node in node_list}
        ppr_weight[source_node] = 1
        
        ppr_dict = nx.pagerank(origin_graph, personalization=ppr_weight)
        
        return ppr_dict
    
    # 境界ノードの PPR 取得
    ppr_dict = {} # 各ノードの PPR を, 辞書の辞書に格納
    
    check_num = 1
    for node in connect_node_list:
        ppr_dict[node] = get_ppr(node)
        print(check_num)
        check_num += 1
    
    print("PPR Calculated!")
    
    return ppr_dict

def return_sampling_graph(graph, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight, ppr_dict):
    sampling_graph = nx.DiGraph()
    if sampling_method == "FC":
        obj = sp.FC()
        sampling_graph = obj.flow_control_sampling_2(graph, sampling_rate, connect_node_list, personalization_dict, default_weight, ppr_dict)
    elif sampling_method == "RE":
        obj = sp.RE()
        sampling_graph = obj.random_edge_sampling(graph, sampling_rate)
    elif sampling_method == "SRW":
        obj = sp.SRW()
        sampling_graph = obj.simple_random_walk_sampling(graph, sampling_rate)
    elif sampling_method == "FF":
        obj = sp.FF()
        sampling_graph = obj.forest_fire_sampling(graph, sampling_rate)
    elif sampling_method == "RPN":
        obj = sp.RPN()
        sampling_graph = obj.random_pagerank_node_sampling(graph, sampling_rate)
    else:
        print("Sampling Error!")
        exit(1)
    
    # 境界ノードとその周辺の出エッジが取得されないと困るので、取得されていない場合は必ずサンプリング割合分だけ取得されるように設定
    for node in connect_node_list:
        if node not in set(list(sampling_graph)):
            sampling_graph.add_node(node)
        out_edge_list = list(graph.successors(node))
        if len(list(sampling_graph.successors(node))) == 0 and len(out_edge_list) != 0:            
            get_out_num = int(len(out_edge_list) * sampling_rate)
            if get_out_num == 0:
                get_out_num = 1
            
            tmp_list = random.sample(out_edge_list, get_out_num)
            for out_node in tmp_list:
                sampling_graph.add_edge(node, out_node)
    
    return sampling_graph

def return_pr_dict(origin_graph, sampling_graph, connect_node_list, default_weight, personalization_dict):    
    pr_weight_origin = {node: default_weight for node in list(origin_graph)}
    pr_weight_sampling = {node: default_weight for node in list(sampling_graph)}
    
    for node in connect_node_list:
        pr_weight_origin[node] = personalization_dict[node]
        pr_weight_sampling[node] = personalization_dict[node]
    
    pr_origin = nx.pagerank(origin_graph, personalization=pr_weight_origin)
    pr_sampling = nx.pagerank(sampling_graph, personalization=pr_weight_sampling)
    
    return pr_origin, pr_sampling

def main_ken():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["RPN", "RE", "FC"]
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    # 描画用パラメータ
    color_list = ["blue", "red", "green"]
    main_title = "ケンドールの順位相関係数"
    x_label = "sampling size"
    y_label = "value"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    
    x_list_list = [rate_list, rate_list, rate_list]
    y_list_list = []
    for sampling in sampling_list:
        ppr_dict = {}
        if sampling == "FC":
            ppr_dict = return_ppr_dict(origin_graph, connect_node_list)
        
        kendall_list = []
        for rate in rate_list:
            sampling_graph = return_sampling_graph(origin_graph, connect_node_list, rate, sampling, personalization_dict, default_weight, ppr_dict)
            pr_origin, pr_sampling = return_pr_dict(origin_graph, sampling_graph, connect_node_list, default_weight, personalization_dict)
            kendall_list.append(Calc.calc_kendall(pr_origin, pr_sampling))
        
        y_list_list.append(kendall_list)
    
    make_plt_ken(x_list_list, y_list_list, x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list)

def main_rmse():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["RPN", "RE", "FC"]
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    top_node_num = 1000 # RMSE を計算する個数範囲
    
    # 描画用パラメータ
    color_list = ["blue", "red", "green"]
    main_title = "RMSE"
    x_label = "sampling size"
    y_label = "value"
    axis = ["plain", "sci"]
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    
    x_list_list = [rate_list, rate_list, rate_list]
    y_list_list = []
    for sampling in sampling_list:
        ppr_dict = {}
        if sampling == "FC":
            ppr_dict = return_ppr_dict(origin_graph, connect_node_list)
        
        rmse_list = []
        for rate in rate_list:
            sampling_graph = return_sampling_graph(origin_graph, connect_node_list, rate, sampling, personalization_dict, default_weight, ppr_dict)
            pr_origin, pr_sampling = return_pr_dict(origin_graph, sampling_graph, connect_node_list, default_weight, personalization_dict)
            rmse_list.append(Calc.calc_rmse_top(pr_origin, pr_sampling, top_node_num))
        
        y_list_list.append(rmse_list)
    
    make_plt_rmse(x_list_list, y_list_list, x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list, axis=axis)

if __name__ == "__main__":
    main_rmse()