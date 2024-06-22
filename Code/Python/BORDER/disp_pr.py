import Calc
import networkx as nx
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
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.close()

def main():
    # ハイパーパラメータ
    graph_name = "slashdot"
    disp_range = 0.001
    
    # 描画パラメータ
    x_label = "Rank"
    y_label = "PR value"
    title = graph_name
    save_path = "../../../Picture/PR分布/{}.png".format(graph_name)
    
    origin_graph = Calc.read_origin_graph(graph_name)
    pr_dict = nx.pagerank(origin_graph)
    pr_sorted = sorted(pr_dict.items(), key=lambda x: x[1], reverse=True)
    
    x_list = []
    y_list = []
    for i, (node, pr) in enumerate(pr_sorted[:int(len(list(origin_graph)) * disp_range)]):
        x_list.append(i+1)
        y_list.append(pr)
    make_plt(x_list, y_list, x_label=x_label, y_label=y_label, title=title, save_path=save_path)
    

if __name__ == "__main__":
    main()