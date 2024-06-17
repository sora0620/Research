import networkx as nx
import Calc
import Sampling as sp
import random
from scipy.stats import kendalltau
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

KENDALL_SUM = 1

def make_plt(x_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
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
    ax.hist(x_list)
    
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

# 個別ノードに関して, ケンドールの順位相関係数を返す
def return_kendall_value(origin_graph, sampling_graph, select_node):
    global KENDALL_SUM
    
    weight_dict_origin = {node: 0 for node in list(origin_graph)}
    weight_dict_origin[select_node] = 1
    weight_dict_sampling = {node: 0 for node in list(sampling_graph)}
    weight_dict_sampling[select_node] = 1
    
    ppr_origin = nx.pagerank(origin_graph, personalization=weight_dict_origin)
    ppr_sampling = nx.pagerank(sampling_graph, personalization=weight_dict_sampling)
    
    ppr_origin_list = []
    ppr_sampling_list = []
    
    for node in list(sampling_graph):
        ppr_origin_list.append(ppr_origin[node])
        ppr_sampling_list.append(ppr_sampling[node])
    
    statistic, pvalue = kendalltau(ppr_origin_list, ppr_sampling_list)
    
    print(f"ケンドール計算 : {KENDALL_SUM} 個終了")
    KENDALL_SUM += 1
    
    return statistic

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_method = "FC"
    weight_node_num = 10
    sampling_rate = 0.5
    weight_range = 2 # 境界ノードの重み幅
    default_weight = 1 # 基本の重み
    
    # 描画用パラメータ
    x_label = "ケンドールの順位相関係数"
    title = graph_name
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    sampling_graph = return_sampling_graph(origin_graph, node_list, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight)
    sampling_node_list = list(sampling_graph)
    
    kendall_list = []
    
    for node in connect_node_list:
        if node in set(sampling_node_list):
            kendall_list.append(return_kendall_value(origin_graph, sampling_graph, node))
    
    make_plt(kendall_list, x_label=x_label, title=title)

if __name__ == "__main__":
    main()