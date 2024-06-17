import networkx as nx
import Calc
import random
import math
import Sampling as sp
import numpy as np
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

USER_FILE = "../../../Dataset/Partition/user/{}.adjlist"
PROVIDER_FILE = "../../../Dataset/Partition/provider/{}.adjlist"
USER_TO_PROVIDER_FILE =  "../../../Dataset/Partition/user_to_provider/{}.txt"
PROVIDER_TO_USER_FILE = "../../../Dataset/Partition/provider_to_user/{}.txt"

# 描画系
def make_plt_1(origin_list, sampled_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
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

# make_plt_1 に渡すリスト作成用の関数
def return_list(origin_graph, sampling_graph, disp_range):
    """
    サンプリング前後のグラフにおける, PR 分布の描画

    Parameters:
        origin_graph (graph): 元グラフ
        sampling_graph (graph): 縮小グラフ
        disp_range (int): PR 値 top N 位の描画範囲 N を指定 
        
    Return:
        origin_list (list (list)): 元グラフのノードの PR 順位と PR 値のリストを格納したリスト
        sampled_list (list (list)): 縮小グラフのノードの PR 順位と PR 値のリストを格納したリスト
    """
    
    node_set_sampled = set(list(sampling_graph))
    
    pr_origin = nx.pagerank(origin_graph)
    pr_sampled = nx.pagerank(sampling_graph)
    pr_origin_sorted = sorted(pr_origin.items(), key=lambda x: x[1], reverse=True)
        
    x_list_before = []
    y_list_before = []
    x_list_after = []
    y_list_after = []
    
    for i in range(disp_range):
        tmp_node = pr_origin_sorted[i][0] # 元グラフ PR 上位 i + 1 番目のノード
        rank = i + 1
        x_list_before.append(rank)
        y_list_before.append(pr_origin_sorted[i][1])
        
        if tmp_node in node_set_sampled:
            x_list_after.append(rank)
            y_list_after.append(pr_sampled[tmp_node])
    
    origin_list = [x_list_before, y_list_before]
    sampled_list = [x_list_after, y_list_after]
    
    return origin_list, sampled_list

# 読み込み
def read_user_to_provider_edge_list(graph_name):
    filename = USER_TO_PROVIDER_FILE.format(graph_name)
    border_edge_list = []
    
    with open(filename, 'r') as f:
        for line in f:
            user_node, provider_node = map(int, line.split())
            border_edge_list.append((user_node, provider_node))
    
    return border_edge_list

def read_provider_to_user_edge_list(graph_name):
    filename = PROVIDER_TO_USER_FILE.format(graph_name)
    border_edge_list = []
    
    with open(filename, 'r') as f:
        for line in f:
            provider_node, user_node = map(int, line.split())
            border_edge_list.append((provider_node, user_node))
    
    return border_edge_list

# 重み系

# 指定した境界ノード数を満たすように, 境界エッジ (user to provider) を取得し, そのリストを返す
# connect_node を選ぶのと似た感じ
def select_border_edge(user_to_provider_edge_list, weight_node_num):
    flag_set = set()
    return_edge_list = []
    
    while True:
        get_edge = random.choice(user_to_provider_edge_list)
        return_edge_list.append(get_edge)
        flag_set.add(get_edge[1])
        
        if len(flag_set) == weight_node_num:
            break
    
    return return_edge_list

def in_rwer_flow(user_graph, select_border_edge_list):
    user_border_node_list = []
    provider_border_node_list = []
    
    user_pr = nx.pagerank(user_graph)
    
    for user_node, provider_node in select_border_edge_list:
        user_border_node_list.append(user_node)
        provider_border_node_list.append(provider_node)
    
    in_rwer_dict = {node: 0 for node in provider_border_node_list} # 返り値とする辞書
    user_rwer_dict = {} # ここに, user 側から provider 側へと流れる RWer を格納
    
    for user_node in user_border_node_list:
        user_rwer_dict[user_node] = user_pr[user_node] / (len(list(user_graph.successors(user_node))) + 1) # 境界エッジの分を考えて, + 1 する
    
    for user_node, provider_node in select_border_edge_list:
        in_rwer_dict[provider_node] += user_rwer_dict[user_node]
    
    return in_rwer_dict

def return_border_weight_dict(in_flow_dict, default_weight):
    return_dict = {}
    
    for node, value in in_flow_dict.items():
        return_dict[node] = value + default_weight
    
    return return_dict

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

# user, provider グラフを接続
# provider グラフが縮小前でも後でも OK な形にする
def return_syn_graph(user_graph, provider_graph, border_edge_list, provider_to_user_edge_list):
    return_graph = nx.DiGraph()
    
    provider_node_set = set(list(provider_graph))
    
    return_graph.add_nodes_from(list(user_graph))
    return_graph.add_nodes_from(list(provider_graph))
    return_graph.add_edges_from(list(user_graph.edges()))
    return_graph.add_edges_from(list(provider_graph.edges()))
    
    return_graph.add_edges_from(border_edge_list)
    
    for provider_node, user_node in provider_to_user_edge_list:
        if provider_node in provider_node_set:
            return_graph.add_edge(provider_node, user_node)
    
    return return_graph

# 分布描画
def main_1():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_method = "RE"
    weight_node_num = 100 # provider 側で重み付けをするノードの個数を設定
    default_weight = 50 # 基本の重み. このコードだと必要無い値なので何に設定しても OK. このためにサンプリングの実装の方を変えちゃうと他のコードが上手くいかなくなるので残しておくが, この実装では, 重みはユーザグラフに従って勝手に決定される
    sampling_rate = 0.2
    disp_range = 1000
    
    # 描画用パラメータ
    x_label = "ノード順位"
    y_label = "PR 合計値"
    axis=["plain", "sci"]
    title = sampling_method
    
    # 読み込み
    user_graph = Calc.read_graph(USER_FILE.format(graph_name))
    provider_graph = Calc.read_graph(PROVIDER_FILE.format(graph_name))
    user_to_provider_edge_list = read_user_to_provider_edge_list(graph_name)
    provider_to_user_edge_list = read_provider_to_user_edge_list(graph_name)
    
    # 重み設定等
    border_edge_list = select_border_edge(user_to_provider_edge_list, weight_node_num) # user to provider の境界エッジを, weight_node_num を満たすように設定して取得
    in_flow_dict = in_rwer_flow(user_graph, border_edge_list)
    border_weight_dict = return_border_weight_dict(in_flow_dict, default_weight)
    connect_node_list = list(in_flow_dict.keys())
    
    # グラフ取得 → provider_graph : origin_graph, sampling_graph : sampling_graph のようなもの
    sampling_graph = return_sampling_graph(provider_graph, connect_node_list, sampling_rate, sampling_method, border_weight_dict, default_weight)
    syn_origin_graph = return_syn_graph(user_graph, provider_graph, border_edge_list, provider_to_user_edge_list)
    syn_sampling_graph = return_syn_graph(user_graph, sampling_graph, border_edge_list, provider_to_user_edge_list)

    origin_list, sampled_list = return_list(syn_origin_graph, syn_sampling_graph, disp_range)
    make_plt_1(origin_list, sampled_list, x_label=x_label, y_label=y_label, title=title, axis=axis)

def main_ken():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["RPN", "RE", "FC"]
    weight_node_num = 100 # provider 側で重み付けをするノードの個数を設定
    default_weight = 50 # 基本の重み. このコードだと必要無い値なので何に設定しても OK. このためにサンプリングの実装の方を変えちゃうと他のコードが上手くいかなくなるので残しておくが, この実装では, 重みはユーザグラフに従って勝手に決定される
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    # 描画用パラメータ
    color_list = ["blue", "red", "green"]
    main_title = "ケンドールの順位相関係数"
    x_label = "sampling size"
    y_label = "value"
    
    # 読み込み
    user_graph = Calc.read_graph(USER_FILE.format(graph_name))
    provider_graph = Calc.read_graph(PROVIDER_FILE.format(graph_name))
    user_to_provider_edge_list = read_user_to_provider_edge_list(graph_name)
    provider_to_user_edge_list = read_provider_to_user_edge_list(graph_name)
    
    # 重み設定等
    border_edge_list = select_border_edge(user_to_provider_edge_list, weight_node_num) # user to provider の境界エッジを, weight_node_num を満たすように設定して取得
    in_flow_dict = in_rwer_flow(user_graph, border_edge_list)
    border_weight_dict = return_border_weight_dict(in_flow_dict, default_weight)
    connect_node_list = list(in_flow_dict.keys())
    
    x_list_list = [rate_list, rate_list, rate_list]
    y_list_list = []
    for sampling in sampling_list:
        ppr_dict = {}
        if sampling == "FC":
            ppr_dict = return_ppr_dict(provider_graph, connect_node_list)
        
        kendall_list = []
        for rate in rate_list:
            # グラフ取得 → provider_graph : origin_graph, sampling_graph : sampling_graph のようなもの
            # provider_graph : 情報提供側での元グラフ
            # sampling_graph : 情報提供側でのサンプリンググラフ
            # syn_origin_graph : ユーザグラフと情報提供側での元グラフを接続したもの
            # syn_sampling_graph : ユーザグラフと情報提供側でのサンプリンググラフを接続したもの
            sampling_graph = return_sampling_graph(provider_graph, connect_node_list, rate, sampling, border_weight_dict, default_weight, ppr_dict)
            syn_origin_graph = return_syn_graph(user_graph, provider_graph, border_edge_list, provider_to_user_edge_list)
            syn_sampling_graph = return_syn_graph(user_graph, sampling_graph, border_edge_list, provider_to_user_edge_list)
            pr_origin = nx.pagerank(syn_origin_graph)
            pr_sampling = nx.pagerank(syn_sampling_graph)
            kendall_list.append(Calc.calc_kendall(pr_origin, pr_sampling))
        
        y_list_list.append(kendall_list)
        
    make_plt_ken(x_list_list, y_list_list, x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list)

def main_rmse():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling_list = ["RPN", "RE", "FC"]
    weight_node_num = 100 # provider 側で重み付けをするノードの個数を設定
    default_weight = 50 # 基本の重み. このコードだと必要無い値なので何に設定しても OK. このためにサンプリングの実装の方を変えちゃうと他のコードが上手くいかなくなるので残しておくが, この実装では, 重みはユーザグラフに従って勝手に決定される
    rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    top_node_num = 1000 # RMSE を計算する個数範囲
    
    # 描画用パラメータ
    color_list = ["blue", "red", "green"]
    main_title = "RMSE"
    x_label = "sampling size"
    y_label = "value"
    axis = ["plain", "sci"]
    
    # 読み込み
    user_graph = Calc.read_graph(USER_FILE.format(graph_name))
    provider_graph = Calc.read_graph(PROVIDER_FILE.format(graph_name))
    user_to_provider_edge_list = read_user_to_provider_edge_list(graph_name)
    provider_to_user_edge_list = read_provider_to_user_edge_list(graph_name)
    
    # 重み設定等
    border_edge_list = select_border_edge(user_to_provider_edge_list, weight_node_num) # user to provider の境界エッジを, weight_node_num を満たすように設定して取得
    in_flow_dict = in_rwer_flow(user_graph, border_edge_list)
    border_weight_dict = return_border_weight_dict(in_flow_dict, default_weight)
    connect_node_list = list(in_flow_dict.keys())
    
    x_list_list = [rate_list, rate_list, rate_list]
    y_list_list = []
    for sampling in sampling_list:
        ppr_dict = {}
        if sampling == "FC":
            ppr_dict = return_ppr_dict(provider_graph, connect_node_list)
        
        rmse_list = []
        for rate in rate_list:
            # グラフ取得 → provider_graph : origin_graph, sampling_graph : sampling_graph のようなもの
            sampling_graph = return_sampling_graph(provider_graph, connect_node_list, rate, sampling, border_weight_dict, default_weight, ppr_dict)
            syn_origin_graph = return_syn_graph(user_graph, provider_graph, border_edge_list, provider_to_user_edge_list)
            syn_sampling_graph = return_syn_graph(user_graph, sampling_graph, border_edge_list, provider_to_user_edge_list)
            pr_origin = nx.pagerank(syn_origin_graph)
            pr_sampling = nx.pagerank(syn_sampling_graph)
            rmse_list.append(Calc.calc_rmse_top(pr_origin, pr_sampling, top_node_num))
        
        y_list_list.append(rmse_list)
        
    make_plt_rmse(x_list_list, y_list_list, x_label=x_label, y_label=y_label, title=main_title, label_list=sampling_list, color_list=color_list, axis=axis)

if __name__ == "__main__":
    main_rmse()