import networkx as nx
import Calc
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要
import json

def read_ppr(path):
    ppr_dict = {}
    return_dict = {}
    
    with open(path, 'r') as f:
        ppr_dict = json.load(f)
    
    for key, value in ppr_dict.items():
        return_dict[int(key)] = value
    
    return return_dict

def make_plt(x_list, y_list, start_x_list, start_y_list, figsize=(6, 6), x_label=None, y_label=None, title=None, axis=["plain", "plain"], save_path=None):
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
    ax.scatter(x_list, y_list, c="blue")
    ax.scatter(start_x_list, start_y_list, c="red")
    
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
    ax.set_xlim(left=0, right=0.1)
    ax.set_ylim(bottom=0, top=0.1)
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.close()

def return_ppr(start_node_list, graph):
    weight_dict = {node: 0 for node in list(graph)}
    # for node in start_node_list:
    #     weight_dict[node] = 1
    for node in start_node_list:
        weight_dict[node] = node + 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    
    return ppr_dict

def main():
    # ハイパーパラメータ
    start_node_list = list(range(10)) # PPR を確かめるノードのノード番号
    graph_name = "soc-Epinions1"
    path = "../../../Dataset/PPR/{}_multi_ppr.json".format(graph_name)
    
    # 描画パラメータ
    x_label = "Networkx の結果"
    y_label = "RWer の結果"
    title = "PPR 結果の比較"

    origin_graph = Calc.read_origin_graph(graph_name)
    ppr_dict = return_ppr(start_node_list, origin_graph)
    ppr_dict_rwer = read_ppr(path)
    
    x_list = []
    y_list = []
    start_x_list = []
    start_y_list = []
    for node in list(origin_graph):
        if node in start_node_list:
            start_x_list.append(ppr_dict[node])
            start_y_list.append(ppr_dict_rwer[node])
        else:
            x_list.append(ppr_dict[node])
            y_list.append(ppr_dict_rwer[node])
    
    make_plt(x_list, y_list, start_x_list, start_y_list, x_label=x_label, y_label=y_label, title=title)

if __name__ == "__main__":
    main()