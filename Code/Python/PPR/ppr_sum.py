import networkx as nx
import Calc
import Sampling as sp
import random
from scipy.stats import kendalltau
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

def make_plt(x_list, y_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
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
    ax.scatter(x_list, y_list)
    
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
    ax.set_xlim(left=0, right=1000)
    ax.set_ylim(bottom=0, top=1000)
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.close()

def make_plt_2(origin_list, sampled_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
    """
    １つのグラフを表示するための関数

    Parameters:
        origin_list (list (list)): 元グラフのノードの PR 順位と PR 値のリストを格納したリスト
        sampled_list (list (list)): 縮小グラフのノードの PR 順位と PR 値のリストを格納したリスト
        figsize (taple): グラフ全体のサイズ
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
        title (string): グラフのタイトル
        axis (string): 軸の表記を設定. "plain" はそのまま, "sci" を指定すると指数表記になる. なお, [x 軸, y 軸] で指定
        save_path (string): .pngとして保存したい場合, パスを指定
    """
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # 元グラフ用
    ax.plot(origin_list[0], origin_list[1], c="red", label="縮小前")
    
    # 縮小グラフ用
    ax.scatter(sampled_list[0], sampled_list[1], c="blue", marker="x", label="縮小後")
    
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

def return_sampling_graph(graph, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight):
    sampling_graph = nx.DiGraph()
    if sampling_method == "FC":
        obj = sp.FC()
        sampling_graph = obj.flow_control_sampling(graph, sampling_rate, connect_node_list, personalization_dict, default_weight)
    elif sampling_method == "RE":
        obj = sp.RE()
        sampling_graph = obj.random_edge_sampling(graph, sampling_rate)
    elif sampling_method == "SRW":
        obj = sp.SRW()
        sampling_graph = obj.simple_random_walk_sampling(graph, sampling_rate)
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

def return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, weight_dict):
    sampling_node_set = set(list(sampling_graph))
    personalization_origin = {node: 0 for node in list(origin_graph)}
    personalization_sampling = {node: 0 for node in list(sampling_graph)}
    
    for node in connect_node_list:
        personalization_origin[node] = weight_dict[node]
        personalization_sampling[node] = weight_dict[node]
    
    ppr_sum_origin = nx.pagerank(origin_graph, personalization=personalization_origin)
    ppr_sum_sampling = nx.pagerank(sampling_graph, personalization=personalization_sampling)

    ppr_origin_sorted = sorted(ppr_sum_origin.items(), key=lambda x: x[1], reverse=True)
    ppr_sampling_sorted = sorted(ppr_sum_sampling.items(), key=lambda x: x[1], reverse=True)
    
    rank_origin = {}
    rank_sampling = {}
    
    rank = 1
    for node, ppr in ppr_origin_sorted:
        if node in sampling_node_set:
            rank_origin[node] = rank
            rank += 1
    
    rank = 1
    for node, ppr in ppr_sampling_sorted:
        rank_sampling[node] = rank
        rank += 1
        
    x_list = []
    y_list = []
    
    for node in sampling_node_set:
        x_list.append(rank_origin[node])
        y_list.append(rank_sampling[node])
    
    return x_list, y_list

def return_ppr_sum_rank_2(origin_graph, sampling_graph, connect_node_list, weight_dict, disp_range):
    node_set_sampled = set(list(sampling_graph))
    personalization_origin = {node: 0 for node in list(origin_graph)}
    personalization_sampling = {node: 0 for node in list(sampling_graph)}
    
    for node in connect_node_list:
        personalization_origin[node] = weight_dict[node]
        personalization_sampling[node] = weight_dict[node]
    
    ppr_sum_origin = nx.pagerank(origin_graph, personalization=personalization_origin)
    ppr_sum_sampling = nx.pagerank(sampling_graph, personalization=personalization_sampling)
    ppr_origin_sorted = sorted(ppr_sum_origin.items(), key=lambda x: x[1], reverse=True)
    
    x_list_before = []
    y_list_before = []
    x_list_after = []
    y_list_after = []
    
    for i in range(disp_range):
        tmp_node = ppr_origin_sorted[i][0] # 元グラフ PR 上位 i + 1 番目のノード
        rank = i + 1
        x_list_before.append(rank)
        y_list_before.append(ppr_origin_sorted[i][1])
        
        if tmp_node in node_set_sampled:
            x_list_after.append(rank)
            y_list_after.append(ppr_sum_sampling[tmp_node])
    
    origin_list = [x_list_before, y_list_before]
    sampled_list = [x_list_after, y_list_after]
    
    return origin_list, sampled_list

# 散布図による描画
def main_1():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_method = "FC"
    weight_node_num = 100
    sampling_rate = 0.2
    weight_range = 2 # 境界ノードの重み幅
    default_weight = 1 # 基本の重み
    
    # 描画用パラメータ
    x_label = "縮小前 PPR 合計順位"
    y_label = "縮小後 PPR 合計順位"
    title = graph_name
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    sampling_graph = return_sampling_graph(origin_graph, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight)
    x_list, y_list = return_ppr_sum_rank(origin_graph, sampling_graph, connect_node_list, personalization_dict)
    make_plt(x_list, y_list, x_label=x_label, y_label=y_label, title=title)

# 分布図による描画
def main_2():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_method = "FC"
    weight_node_num = 100
    sampling_rate = 0.2
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    disp_range = 1000 # 描画範囲
    
    # 描画用パラメータ
    x_label = "rank"
    y_label = "Multi-Source PPR"
    axis=["plain", "sci"]
    title = sampling_method
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    sampling_graph = return_sampling_graph(origin_graph, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight)
    x_list, y_list = return_ppr_sum_rank_2(origin_graph, sampling_graph, connect_node_list, personalization_dict, disp_range)
    make_plt_2(x_list, y_list, x_label=x_label, y_label=y_label, title=title, axis=axis)

if __name__ == "__main__":
    main_2()