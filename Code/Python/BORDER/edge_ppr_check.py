import networkx as nx
import Calc
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要
import json

def read_edge_ppr(path):
    edge_ppr_dict = {}
    return_dict = {}
    
    with open(path, 'r') as f:
        edge_ppr_dict = json.load(f)
    
    for key, value in edge_ppr_dict.items():
        source, target = map(int, key.split())
        return_dict[(source, target)] = value
    
    return return_dict

def read_ppr(path):
    ppr_dict = {}
    return_dict = {}
    
    with open(path, 'r') as f:
        ppr_dict = json.load(f)
    
    for key, value in ppr_dict.items():
        return_dict[int(key)] = value
    
    return return_dict

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
    ax.set_xlim(left=0, right=0.0004)
    ax.set_ylim(bottom=0, top=0.0004)
    
    plt.tight_layout()
    # plt.show()
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    plt.close()

def return_edge_ppr(start_node, graph):
    weight_dict = {node: 0 for node in list(graph)}
    weight_dict[start_node] = 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    return_dict = {}
    for node in list(graph):
        out_deg = graph.out_degree(node)
        for adj_node in list(graph.successors(node)):
            return_dict[(node, adj_node)] = ppr_dict[node] / out_deg
    
    return return_dict

def return_ppr(node, graph):
    weight_dict = {node: 0 for node in list(graph)}
    weight_dict[node] = 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    
    return ppr_dict

# PPR を取得してからエッジ PPR にしたもの
def main_ppr():
    # ハイパーパラメータ
    start_node = 0 # PPR を確かめるノードのノード番号
    graph_name = "soc-Epinions1"
    path = "../../../Dataset/Centrality/ppr.json"
    save_file = "../pic/check_edge_ppr.png"
    
    # 描画パラメータ
    x_label = "Python の結果"
    y_label = "C++ の結果"
    title = "edge_PPR 結果の比較"

    origin_graph = Calc.read_origin_graph(graph_name)
    ppr_dict_python = return_ppr(start_node, origin_graph)
    ppr_dict_c = read_ppr(path)
    
    edge_ppr_dict_python = {}
    edge_ppr_dict_c = {}
    for node in list(origin_graph):
        for adj_node in list(origin_graph.successors(node)):
            edge_ppr_dict_python[(node, adj_node)] = ppr_dict_python[node] / len(list(origin_graph.successors(node)))
            edge_ppr_dict_c[(node, adj_node)] = ppr_dict_c[node] / len(list(origin_graph.successors(node)))
    
    x_list = []
    y_list = []
    for node in list(origin_graph):
        for adj_node in list(origin_graph.successors(node)):
            x_list.append(edge_ppr_dict_python[(node, adj_node)])
            y_list.append(edge_ppr_dict_c[(node, adj_node)])
    
    make_plt(x_list, y_list, x_label=x_label, y_label=y_label, title=title, save_path=save_file)

# 直接 C++ のエッジ PPR データを取得
def main_edge_ppr():
    # ハイパーパラメータ
    start_node = 0 # PPR を確かめるノードのノード番号
    graph_name = "soc-Epinions1"
    path = "../../../Dataset/Centrality/edge_ppr.json"
    save_file = "../pic/check_edge_ppr.png"
    
    # 描画パラメータ
    x_label = "Python の結果"
    y_label = "C++ の結果"
    title = "edge_PPR 結果の比較"

    origin_graph = Calc.read_origin_graph(graph_name)
    ppr_dict_python = return_ppr(start_node, origin_graph)
    edge_ppr_dict_c = read_edge_ppr(path)
    
    edge_ppr_dict_python = {}
    for node in list(origin_graph):
        for adj_node in list(origin_graph.successors(node)):
            edge_ppr_dict_python[(node, adj_node)] = ppr_dict_python[node] / len(list(origin_graph.successors(node)))
    
    x_list = []
    y_list = []
    for node in list(origin_graph):
        for adj_node in list(origin_graph.successors(node)):
            x_list.append(edge_ppr_dict_python[(node, adj_node)])
            y_list.append(edge_ppr_dict_c[(node, adj_node)])
    sum_python = 0
    sum_c = 0
    for key, value in edge_ppr_dict_python.items():
        sum_python += value
    for key, value in edge_ppr_dict_c.items():
        sum_c += value
    print(f"Python Sum: {sum_python}")
    print(f"C++ Sum: {sum_c}")
    
    make_plt(x_list, y_list, x_label=x_label, y_label=y_label, title=title, save_path=save_file)

if __name__ == "__main__":
    main_edge_ppr()