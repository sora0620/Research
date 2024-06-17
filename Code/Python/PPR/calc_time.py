import networkx as nx
import Sampling as sp
import random
import time
import Calc
import numpy as np
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

def make_plt(x_list, value_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis="plain", save_path=None, labels=None):
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
    
    if labels != None:
        ax.bar(x_list, value_list, tick_label=labels, width=0.5)
    else:
        print("Error!")
        exit(1)
    
    # ax の設定
    if title != None:
        ax.set_title(title)
    if x_label != None:
        ax.set_xlabel(x_label)
    if y_label != None:
        ax.set_ylabel(y_label)
    ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style=axis, axis="y", scilimits=(0,0))
    
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
    tim = 0
    
    if sampling_method == "FC":
        obj = sp.FC()
        time_start = time.perf_counter()
        
        sampling_graph = obj.flow_control_sampling_2(graph, sampling_rate, connect_node_list, personalization_dict, default_weight, ppr_dict)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
    elif sampling_method == "SRW":
        obj = sp.SRW()
        time_start = time.perf_counter()
        
        sampling_graph = obj.simple_random_walk_sampling(graph, sampling_rate)
        
        time_end = time.perf_counter()
        tim = time_end - time_start
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
    
    return sampling_graph, tim

def main():
    # ハイパーパラメータ
    graph_name = "scale_free"
    sampling_list = ["SRW", "FC"]
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    sampling_rate = 0.1 # サンプリングサイズ
    
    # 描画パラメータ
    x_label = "Sampling Method"
    y_label = "Time"
    title = "実行時間比較"
    
    time_list = []
    name_list = []
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    connect_node_list = random.sample(node_list, weight_node_num)
    personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
    
    for sampling in sampling_list:
        ppr_dict = {}
        ppr_calc_time = 0
        
        if sampling == "FC":
            time_start = time.perf_counter()
            
            ppr_dict = return_ppr_dict(origin_graph, connect_node_list)
            
            time_end = time.perf_counter()
            ppr_calc_time = time_end - time_start
            
        sampling_graph, tim = return_sampling_graph(origin_graph, connect_node_list, sampling_rate, sampling, personalization_dict, default_weight, ppr_dict)
        
        if sampling == "FC":
            name_list.append(f"{sampling}_no-cache")
            name_list.append(f"{sampling}_cached")
            time_list.append(tim+ppr_calc_time)
            time_list.append(tim)
        else:
            name_list.append(sampling)
            time_list.append(tim)
    
    x_list = np.arange(len(name_list))
    make_plt(x_list, time_list, x_label=x_label, y_label=y_label, title=title, labels=name_list)

if __name__ == "__main__":
    main()