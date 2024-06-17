import networkx as nx
import Calc
import Sampling as sp
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要
import math
import random

ORIGIN_FILE = "../../../Dataset/Origin/{}.adjlist"
SAMPLING_FILE = "../../../Dataset/Partition/div_3/{}/sub_{}.adjlist"

def make_plt(x_list_list, y_list_list, color_list=None, figsize=(10, 10), main_title=None, subtitle_list=None, x_label=None, y_label=None, axis=["plain", "plain"], save_path=None):
    """
    複数のグラフを表示するための関数
    左上から右下に向かって順番に描画
    
    Parameters:
        x_list_list, y_list_list (listのlist): 表示したいデータ群を, 各々リストに格納 (各インデックスが対応)
        color_list (listのlist (string)): ノード毎に色を変えたい場合, 各ノードに対して色を設定したリストを渡せば, 各ノード毎に色を設定可能
        figsize (taple): グラフ全体のサイズ
        main_title (string): グラフ全体のタイトル
        subtitle_list (list (string)): 各グラフのタイトルをリストに格納
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
        axis (string): 軸の表記を設定. "plain" はそのまま, "sci" を指定すると指数表記になる. なお, [x 軸, y 軸] で指定
        save_path (string): .pngとして保存したい場合, パスを指定
    """
    
    # pltサイズの決定
    graph_num = len(x_list_list)
    column = 0 # 縦
    row = 0 # 横
    
    if graph_num == 0:
        print("List Empty Error!")
        exit(1)
    else:
        if math.isqrt(graph_num)**2 == graph_num:
            row = math.isqrt(graph_num)
        else:
            row = int(math.sqrt(graph_num)) + 1
            
        column = math.ceil(graph_num / row)
    
    fig, ax = plt.subplots(column, row, figsize=figsize)
    
    # ax の設定
    for i in range(graph_num):
        ax_y = int(i / row)
        ax_x = i - ax_y * row
        tmp_ax = ax[ax_x, ax_y]
        if subtitle_list != None:
            tmp_ax.set_title(subtitle_list[i])
        if x_label != None:
            tmp_ax.set_xlabel(x_label)
        if y_label != None:
            tmp_ax.set_ylabel(y_label)
        tmp_ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        tmp_ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        tmp_ax.ticklabel_format(style=axis[0], axis="x", scilimits=(0,0))
        tmp_ax.ticklabel_format(style=axis[1], axis="y", scilimits=(0,0))
        
        if color_list != None:
            tmp_ax.scatter(x_list_list[i], y_list_list[i], c=color_list, s=5)
        else:
            tmp_ax.scatter(x_list_list[i], y_list_list[i], s=5)
        m = max(max(x_list_list[i]), max(y_list_list[i]))
        tmp_ax.plot(list(range(m)), list(range(m)))

    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    if main_title != None:
        fig.suptitle(main_title)
    plt.tight_layout()
    plt.show()
    plt.close()

def make_plt_2(x_list, y_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
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
    color_list = ["red", "green", "yellow"]
    for i in range(len(x_list)):
        ax.scatter(x_list[i], y_list[i], c=color_list[i], s=10)
        
    max_rank = 0
    for i in range(len(x_list)):
        max_x = max(x_list[i])
        max_y = max(y_list[i])
        if max_x > max_rank:
            max_rank = max_x
        if max_y > max_rank:
            max_rank = max_y
    
    # ax の設定
    if title != None:
        ax.set_title(title)
    if x_label != None:
        ax.set_xlabel(x_label)
    if y_label != None:
        ax.set_ylabel(y_label)
    ax.set_xlim(right=max_rank, left=0)
    ax.set_ylim(top=max_rank, bottom=0)
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

def read_com_graph(com_size, graph_name):
    graph_list = []
    
    for i in range(com_size):
        path = SAMPLING_FILE.format(graph_name, i)
        tmp_graph = Calc.read_graph(path)
        graph_list.append(tmp_graph)
    
    return  graph_list

def return_sampling_graph(graph_list, sampling_rate):
    return_list = []
    
    for i in range(len(graph_list)):
        tmp_graph = graph_list[i]
        graph_size = int(len(list(tmp_graph)) * sampling_rate)
        pr = nx.pagerank(tmp_graph)
        obj = sp.TPN()
        sp_graph = obj.top_pagerank_sampling(tmp_graph, graph_size, pr)
        return_list.append(sp_graph)
    
    return return_list

# 各コミュニティ間のエッジは自然接続
def synthesys_graph_1(origin_graph, sampling_graph_list):
    sampling_node_set = set()
    
    for sampling_graph in sampling_graph_list:
        sampling_node_set.update(set(list(sampling_graph)))
    
    return_graph = origin_graph.subgraph(list(sampling_node_set))
    
    return return_graph

# 各コミュニティ間のエッジを、元グラフに存在するエッジで接続
def synthesys_graph_2(origin_graph, com_graph_list, sampling_graph_list):
    sampling_node_set = set()
    
    com_in_edge = set()
    
    for tmp_graph in com_graph_list:
        com_in_edge.update(set(list(tmp_graph.edges)))
    
    com_edge = set(list(origin_graph.edges)) - com_in_edge # コミュニティ間に存在するエッジ全ての集合
    
    for sampling_graph in sampling_graph_list:
        sampling_node_set.update(set(list(sampling_graph)))
    
    tmp_graph = origin_graph.subgraph(list(sampling_node_set))
    return_graph = tmp_graph.to_directed()
    return_graph.add_edges_from(list(com_edge))
    
    return return_graph

def make_disp_list(origin_graph, sampling_graph, sampling_graph_list, weight_range, bias_node_rate):
    sampling_node_list = [] # 各コミュニティにおける縮小後のノードを各々で取得. 各要素は set 型
    all_sampling_node_list = list(sampling_graph) # グラフ縮小後の全ノードのリスト
    sampling_node_num = len(all_sampling_node_list) # 縮小グラフのノード数
    bias_node_num = int(sampling_node_num * bias_node_rate) # 重み付けするノードの数
    node_weight_origin = {}
    node_weight_sampling = {}
    com_size = len(sampling_graph_list)
    
    x_list_list = []
    y_list_list = []
    
    for tmp_graph in sampling_graph_list:
        sampling_node_list.append(set(list(tmp_graph)))
    
    # 縮小後グラフに存在する全ノードに対して各々重みを設定
    # 範囲に注意
    for node in list(origin_graph):
        node_weight_origin[node] = 1
    for node in all_sampling_node_list:
        node_weight_sampling[node] = 1
    
    bias_node_list = random.sample(all_sampling_node_list, bias_node_num) # 重み付けするノードを, 縮小後グラフから選択
    for node in bias_node_list:
        randint = random.randint(2, weight_range)
        node_weight_origin[node] = randint
        node_weight_sampling[node] = randint
    
    pr_origin = nx.pagerank(origin_graph, personalization=node_weight_origin)
    pr_sampling = nx.pagerank(sampling_graph, personalization=node_weight_sampling)
    
    pr_origin_sorted = sorted(pr_origin.items(), key=lambda x: x[1], reverse=True)
    pr_sampling_sorted = sorted(pr_sampling.items(), key=lambda x: x[1], reverse=True)
    
    for i in range(com_size):
        rank_origin = {}
        rank_sampling = {}
        
        rank = 1
        for node, pr in pr_origin_sorted:
            if node in sampling_node_list[i]:
                rank_origin[node] = rank
                rank += 1
        
        rank = 1
        for node, pr in pr_sampling_sorted:
            if node in sampling_node_list[i]:
                rank_sampling[node] = rank
                rank += 1
            
        x_list = []
        y_list = []
        
        for node in sampling_node_list[i]:
            x_list.append(rank_origin[node])
            y_list.append(rank_sampling[node])
        
        x_list_list.append(x_list)
        y_list_list.append(y_list)
    
    return x_list_list, y_list_list

def make_disp_list_2(origin_graph, sampling_graph, sampling_graph_list, weight_range, bias_node_rate, top_N):
    sampling_node_list = [] # 各コミュニティにおける縮小後のノードを各々で取得. 各要素は set 型
    all_sampling_node_list = list(sampling_graph) # グラフ縮小後の全ノードのリスト
    sampling_node_num = len(all_sampling_node_list) # 縮小グラフのノード数
    bias_node_num = int(sampling_node_num * bias_node_rate) # 重み付けするノードの数
    node_weight_origin = {}
    node_weight_sampling = {}
    com_size = len(sampling_graph_list)
    
    x_list = []
    y_list = []
    
    for tmp_graph in sampling_graph_list:
        sampling_node_list.append(set(list(tmp_graph)))
    
    # 縮小後グラフに存在する全ノードに対して各々重みを設定
    # 範囲に注意
    for node in list(origin_graph):
        node_weight_origin[node] = 1
    for node in all_sampling_node_list:
        node_weight_sampling[node] = 1
    
    bias_node_list = random.sample(all_sampling_node_list, bias_node_num) # 重み付けするノードを, 縮小後グラフから選択
    for node in bias_node_list:
        randint = random.randint(2, weight_range)
        node_weight_origin[node] = randint
        node_weight_sampling[node] = randint
    
    pr_origin = nx.pagerank(origin_graph, personalization=node_weight_origin)
    pr_sampling = nx.pagerank(sampling_graph, personalization=node_weight_sampling)
    
    pr_origin_sorted = sorted(pr_origin.items(), key=lambda x: x[1], reverse=True)
    pr_sampling_sorted = sorted(pr_sampling.items(), key=lambda x: x[1], reverse=True)
    
    top_N_node_list = [] # 各コミュニティ毎に, top_N ノードを格納
    
    for i in range(com_size):
        add_node_list = []
        
        flag = 1
        for node, pr in pr_sampling_sorted:
            if node in sampling_node_list[i]:
                add_node_list.append(node)
                flag += 1
            if flag == top_N + 1:
                break
            
        top_N_node_list.append(add_node_list)
    
    # 縮小前後での, 縮小グラフに存在するノードの順位を取得
    rank_origin = {}
    rank_sampling = {}
    
    rank = 1
    for node, pr in pr_origin_sorted:
        if node in all_sampling_node_list:
            rank_origin[node] = rank
            rank += 1
    
    rank = 1
    for node, pr in pr_sampling_sorted:
        rank_sampling[node] = rank
        rank += 1
    
    for tmp_list in top_N_node_list:
        tmp_x = []
        tmp_y = []
        for node in tmp_list:
            tmp_x.append(rank_origin[node])
            tmp_y.append(rank_sampling[node])
        x_list.append(tmp_x)
        y_list.append(tmp_y)
    
    return x_list, y_list

# 各コミュニティ間のエッジは自然接続
def main_1():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    com_size = 3
    sampling_rate = 0.01
    weight_range = 2
    bias_node_rate = 0.5
    
    # 描画用
    x_label = "縮小前"
    y_label = "縮小後"
    subtitle_list = ["com_0", "com_1", "com_2"]
    
    for graph_name in graph_list:
        # 描画用
        main_title = "{}".format(graph_name)
        
        origin_graph = Calc.read_graph(ORIGIN_FILE.format(graph_name))
        com_graph_list = read_com_graph(com_size, graph_name)
        sampling_graph_list = return_sampling_graph(com_graph_list, sampling_rate)
        sampling_graph = synthesys_graph_1(origin_graph, sampling_graph_list)
        x_list_list, y_list_list = make_disp_list(origin_graph, sampling_graph, sampling_graph_list, weight_range, bias_node_rate)
        make_plt(x_list_list, y_list_list, x_label=x_label, y_label=y_label, main_title=main_title, subtitle_list=subtitle_list)

# 各コミュニティ間のエッジを、元グラフに存在するエッジで接続
def main_2():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    com_size = 3
    sampling_rate = 0.01
    weight_range = 2
    bias_node_rate = 0.5
    
    # 描画用
    x_label = "縮小前"
    y_label = "縮小後"
    subtitle_list = ["com_0", "com_1", "com_2"]
    
    for graph_name in graph_list:
        # 描画用
        main_title = "{}".format(graph_name)
        
        origin_graph = Calc.read_graph(ORIGIN_FILE.format(graph_name))
        com_graph_list = read_com_graph(com_size, graph_name)
        sampling_graph_list = return_sampling_graph(com_graph_list, sampling_rate)
        sampling_graph = synthesys_graph_2(origin_graph, com_graph_list, sampling_graph_list)
        x_list_list, y_list_list = make_disp_list(origin_graph, sampling_graph, sampling_graph_list, weight_range, bias_node_rate)
        make_plt(x_list_list, y_list_list, x_label=x_label, y_label=y_label, main_title=main_title, subtitle_list=subtitle_list)

# 全体に対して各コミュニティ内の top_N がどの程度の順位になるかを比較
def main_3():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    com_size = 3
    sampling_rate = 0.01
    weight_range = 2
    bias_node_rate = 0.5
    top_N = 80
    
    # 描画用
    x_label = "縮小前"
    y_label = "縮小後"
    
    for graph_name in graph_list:
        # 描画用
        main_title = "{}".format(graph_name)
        
        origin_graph = Calc.read_graph(ORIGIN_FILE.format(graph_name))
        com_graph_list = read_com_graph(com_size, graph_name)
        sampling_graph_list = return_sampling_graph(com_graph_list, sampling_rate)
        sampling_graph = synthesys_graph_1(origin_graph, sampling_graph_list)
        x_list, y_list = make_disp_list_2(origin_graph, sampling_graph, sampling_graph_list, weight_range, bias_node_rate, top_N)
        make_plt_2(x_list, y_list, x_label=x_label, y_label=y_label, title=main_title)

if __name__ == "__main__":
    main_3()