import networkx as nx
import random
import matplotlib.pyplot as plt # 描画用
import japanize_matplotlib # 日本語表記を可能にする
import matplotlib.ticker as ptick # 指数表記にするために必要

FILE_NAME = "../../../Dataset/Origin/{}.adjlist"

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

def violinplot_plt(list_list, figsize=(6, 6), x_label=None, y_label=None, data_name_list=None, title=None, xlim=None, axis=["plain"], save_path=None):
    """
    １つのグラフを箱ひげ図で表示するための関数.
    横向きの箱ひげ図な事に注意

    Parameters:
        list_list (list (list (int))): 表示したいデータ群をリストに格納したやつを, 更にリストに格納
        figsize (taple): グラフ全体のサイズ
        graph_label (string): グラフの凡例 (名前表示)
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
        data_name_list (list (string)): 各箱ひげ図が何を表すかといった名称
        title (string): グラフのタイトル
        axis (string): 軸の表記を設定. "plain" はそのまま, "sci" を指定すると指数表記になる
        save_path (string): .pngとして保存したい場合, パスを指定
    """
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.violinplot(list_list, vert=False)
    
    # ax の設定
    if title != None:
        ax.set_title(title)
    if x_label != None:
        ax.set_xlabel(x_label)
    if y_label != None:
        ax.set_ylabel(y_label)
    if data_name_list != None:
        ax.set_yticks(range(1, len(list_list) + 1), labels=data_name_list)
    ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style=axis[0], axis="x", scilimits=(0,0))
    ax.invert_yaxis()
    if xlim != None:
        ax.set_xlim(-xlim, xlim)
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.grid()
    plt.show()
    plt.close()

# グラフ自体を描画
# 重みと重み付けノードの個数を個別に指定
# 横軸に元の順位, 縦軸に全ノードに対して重み付け後の順位を散布図で表示
def disp_1(graph, node_rate, weight_range):
    node_list = list(graph)
    random_node_list = random.sample(node_list, int(len(node_list) * node_rate))
    weight_dict = {}
    
    for node in node_list:
        weight_dict[node] = 1
    
    for node in random_node_list:
        weight_dict[node] = random.randint(2, weight_range)
    
    biased_pr = nx.pagerank(graph, personalization=weight_dict)
    
    default_pr = nx.pagerank(graph)
    default_sorted = sorted(default_pr.items(), key=lambda x: x[1], reverse=True)
    biased_sorted = sorted(biased_pr.items(), key=lambda x: x[1], reverse=True)
    
    rank_dict = {}
    
    for node in list(graph):
        rank_dict[node] = [0, 0]
    
    i = 1
    for node, pr in default_sorted:
        rank_dict[node][0] = i
        i += 1
    
    i = 1
    for node, pr in biased_sorted:
        rank_dict[node][1] = i
        i += 1
    
    x_list = []
    y_list = []
    
    for node in list(graph):
        x_list.append(rank_dict[node][0])
        y_list.append(rank_dict[node][1])
    
    plt.scatter(x_list, y_list)
    plt.show()

# 重みを x 軸, 順位変化を y 軸に取っている. y の値が大きいほど順位が高くなったことを意味する
# disp_1 から軸の設定を変えたやつ
# 全ノードの重みをランダムに決定
def disp_2(graph_name, graph, weight_range):
    node_list = list(graph)
    weight_dict = {}
    
    for node in node_list:
        weight_dict[node] = random.randint(1, weight_range)
    
    biased_pr = nx.pagerank(graph, personalization=weight_dict)

    default_pr = nx.pagerank(graph)
    default_sorted = sorted(default_pr.items(), key=lambda x: x[1], reverse=True)
    biased_sorted = sorted(biased_pr.items(), key=lambda x: x[1], reverse=True)
    
    rank_dict = {}
    
    for node in list(graph):
        rank_dict[node] = [0, 0]
    
    i = 1
    for node, pr in default_sorted:
        rank_dict[node][0] = i
        i += 1
    
    i = 1
    for node, pr in biased_sorted:
        rank_dict[node][1] = i
        i += 1
    
    x_list = []
    y_list = []
    
    for node in list(graph):
        x_list.append(weight_dict[node])
        y_list.append(rank_dict[node][0] - rank_dict[node][1])
    
    # ハイパーパラメータ
    x_label = "重み"
    y_label = "順位変化"
    title  = f"{graph_name}"
    
    make_plt(x_list, y_list, x_label=x_label, y_label=y_label, title=title)

# こっちは PR 変化を縦軸にした
def disp_2_2(graph, weight_range):
    node_list = list(graph)
    weight_dict = {}
    
    for node in node_list:
        weight_dict[node] = random.randint(1, weight_range)
    
    biased_pr = nx.pagerank(graph, personalization=weight_dict)
    default_pr = nx.pagerank(graph)
        
    x_list = []
    y_list = []
    
    for node in list(graph):
        x_list.append(weight_dict[node])
        y_list.append(biased_pr[node] - default_pr[node])
    
    plt.scatter(x_list, y_list)
    plt.show()

# disp_1 の順位変動の具合を, どれだけのノード数に対して重み付けをするかに対しての結果を描画するため、複数のバイオリン図で表示してみる
def disp_1_violin(graph_name, graph, weight_range, xlim):
    node_list = list(graph)
    default_pr = nx.pagerank(graph)
    default_sorted = sorted(default_pr.items(), key=lambda x: x[1], reverse=True)
    
    def return_rank_diff_list(node_rate):
        random_node_list = random.sample(node_list, int(len(node_list) * node_rate))
        weight_dict = {}
        return_list = []
        
        for node in node_list:
            weight_dict[node] = 1
        
        for node in random_node_list:
            weight_dict[node] = random.randint(2, weight_range)
        
        biased_pr = nx.pagerank(graph, personalization=weight_dict)
        biased_sorted = sorted(biased_pr.items(), key=lambda x: x[1], reverse=True)
        
        rank_dict = {}
        
        for node in list(graph):
            rank_dict[node] = [0, 0]
        
        i = 1
        for node, pr in default_sorted:
            rank_dict[node][0] = i
            i += 1
        
        i = 1
        for node, pr in biased_sorted:
            rank_dict[node][1] = i
            i += 1
        
        for node in node_list:
            return_list.append(rank_dict[node][0] - rank_dict[node][1])
        
        return return_list
    
    violin_list = []
    data_name_list = []
    
    for node_rate in range(1, 11, 1):
        node_rate *= 0.1
        violin_list.append(return_rank_diff_list(node_rate))
        data_name_list.append(f"{node_rate:.1f}")
    
    title = f"{graph_name}_重み幅_{weight_range}"
    violinplot_plt(violin_list, figsize=(6, 6), x_label="順位の変動度合い", y_label=None, data_name_list=data_name_list, title=title, axis=["plain"], xlim=xlim, save_path=None)

def main():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    node_rate = 0.1 # 重みをつけるノード数を選択する割合
    weight_range = 100
    xlim = 400000

    for graph_name in graph_list:
        graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
        # disp_1(graph, node_rate, weight_range)
        disp_1_violin(graph_name, graph, weight_range, xlim)
        # disp_2(graph_name, graph, weight_range)
        # disp_2_2(graph, weight_range)
        
if __name__ == "__main__":
    main()