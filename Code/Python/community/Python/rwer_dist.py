import networkx as nx
import Calc
import random
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

READ_FILE = "../../../Dataset/Origin/{}.adjlist"

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
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.close()

def read_graph(graph_name):
    path = READ_FILE.format(graph_name)
    return_graph = Calc.read_graph(path)
    
    return return_graph

def select_one_node(node_list):
    select_node = random.choice(node_list)
    
    return select_node

def calc_ppr(graph, select_node):
    weight_dict = {}
    node_list = list(graph)
    
    for node in node_list:
        weight_dict[node] = 0
    weight_dict[select_node] = 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    
    return ppr_dict

def make_list(graph, select_node, ppr_dict):
    x_list = [] # 選択ノードからの距離を格納
    y_list = [] # PPR 値を格納
    
    node_list = list(graph)
    shortest_path_dict = nx.shortest_path_length(graph, source=select_node)
    
    for node in node_list:
        if shortest_path_dict.get(node) == None:
            x_list.append(0)
        else:
            x_list.append(shortest_path_dict[node])
        y_list.append(ppr_dict[node])
    
    return x_list, y_list

def main():
    # ハイパーパラメータ
    graph_list = ["soc-Epinions1"]
    
    # 描画パラメータ
    x_label = "ノードからの距離"
    y_label = "PPR"
    axis = ["plain", "sci"]
    
    for graph_name in graph_list:
        title = f"{graph_name}"
        origin_graph = read_graph(graph_name)
        node_list = list(origin_graph)
        select_node = select_one_node(node_list)
        ppr_dict = calc_ppr(origin_graph, select_node)
        x_list, y_list = make_list(origin_graph, select_node, ppr_dict)
        make_plt(x_list, y_list, x_label=x_label, y_label=y_label, axis=axis, title=title)
    
if __name__ == "__main__":
    main()