import networkx as nx
import random
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

FILE_NAME = "../../../Dataset/Origin/{}.adjlist"

def calc_bias_pr(graph, weight, bias_node):
    """
    任意の 1 ノードに対して重み付けをし, その PR 計算結果を返す

    Parameters:
        graph (DiGraph): 対象グラフ
        weight (int): 任意の 1 ノードに設定する重み
        bias_node (int): 重み付けるノード ID

    Returns:
        bias_pr (dict (int:float)): 任意の 1 ノードの重みをweightで設定した際の pr 結果
    """
    
    node_list = list(graph)
    
    weight_dict = {}
    
    for node in node_list:
        weight_dict[node] = 1
    
    weight_dict[bias_node] = weight
    
    bias_pr = nx.pagerank(graph, personalization=weight_dict)
    
    return bias_pr

# パターン 1 : シンプルなやつ
def return_list_1(graph, weight):
    """
    重み付けをする任意の 1 ノードを決定後, 
    そのノードからの他全ノードに対する距離と, 重み付け前後の PR 増加量を計算し, 
    描画できるように, x には距離, y には増加量を各ノードに対応させた形で保存

    Parameters:
        graph (DiGraph): 対象グラフ
        weight (int): 任意の 1 ノードに設定する重み

    Returns:
        return_x_list, return_y_list (list (int と float)): x の方は距離のリスト, y の方は PR 増加量のリスト
    """
    
    node_list = list(graph)
    
    bias_node = random.choice(node_list)
    shortest_path_dict = nx.shortest_path_length(graph, source=bias_node)
    
    default_pr = nx.pagerank(graph)
    bias_pr = calc_bias_pr(graph, weight, bias_node)
    
    return_x_list = []
    return_y_list = []
    
    for node in node_list:
        if shortest_path_dict.get(node) == None:
            return_x_list.append(0)
        else:
            return_x_list.append(shortest_path_dict[node])
        return_y_list.append(bias_pr[node] - default_pr[node])
    
    return return_x_list, return_y_list

# パターン２ : 自身の距離が遠くても, そのノードの入隣接の距離が近ければ, そこから影響を受けて意外と PR 増加量が大きくなるのでは？という発想 
def return_list_2(graph, weight):
    """
    重み付けをする任意の 1 ノードを決定後, 
    そのノードと他全ノードとの距離 or 入隣接ノードとの距離の最小値と, 重み付け前後の PR 増加量を計算し, 
    描画できるように, x には自身の距離 or 入隣接の距離の最小値, y には増加量を各ノードに対応させた形で保存

    Parameters:
        graph (DiGraph): 対象グラフ
        weight (int): 任意の 1 ノードに設定する重み

    Returns:
        return_x_list, return_y_list (list (int と float)): x の方は距離のリスト, y の方は PR 増加量のリスト
    """
    
    node_list = list(graph)
    
    bias_node = random.choice(node_list)
    shortest_path_dict = nx.shortest_path_length(graph, source=bias_node)
    
    default_pr = nx.pagerank(graph)
    bias_pr = calc_bias_pr(graph, weight, bias_node)
    
    return_x_list = []
    return_y_list = []
    
    for node in node_list:
        if shortest_path_dict.get(node) == None and len(list(graph.predecessors(node))) == 0:
            return_x_list.append(0)
        else:
            dist_list = []
            for neighbor_node in list(graph.predecessors(node)):
                dist_list.append(shortest_path_dict[neighbor_node])
            if shortest_path_dict.get(node) != None:
                dist_list.append(shortest_path_dict[node])
            return_x_list.append(min(dist_list))
        return_y_list.append(bias_pr[node] - default_pr[node])
    
    return return_x_list, return_y_list

# パターン 3 : パターン 1 で, 横軸を "増加量" から "増加率" に変更したやつ
def return_list_3(graph, weight):
    """
    重み付けをする任意の 1 ノードを決定後, 
    そのノードからの他全ノードに対する距離と, 重み付け前後の PR 増加率 (重み付け後 PR - 重み付け前 PR) / 重み付け前 PR を計算し, 
    描画できるように, x には距離, y には増加率を各ノードに対応させた形で保存

    Parameters:
        graph (DiGraph): 対象グラフ
        weight (int): 任意の 1 ノードに設定する重み

    Returns:
        return_x_list, return_y_list (list (int と float)): x の方は距離のリスト, y の方は PR 増加率のリスト
    """
    
    node_list = list(graph)
    
    bias_node = random.choice(node_list)
    shortest_path_dict = nx.shortest_path_length(graph, source=bias_node)
    
    default_pr = nx.pagerank(graph)
    bias_pr = calc_bias_pr(graph, weight, bias_node)
    
    return_x_list = []
    return_y_list = []
    
    for node in node_list:
        if shortest_path_dict.get(node) == None:
            return_x_list.append(0)
        else:
            return_x_list.append(shortest_path_dict[node])
        return_y_list.append((bias_pr[node] - default_pr[node]) / default_pr[node])
    
    return return_x_list, return_y_list

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
    # ax.set_xlim(right=10)
    
    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    
    plt.tight_layout()
    plt.show()
    plt.close()

# パターン 1 の実行関数
def main_1():
    # ハイパーパラメータ
    graph_list = ["com"]
    # graph_list = ["amazon0601"]
    weight = 2 # RW開始数の重み
    
    # グラフ描画用設定
    figsize = (6, 6)
    x_label = "重み付けしたノードからの距離"
    y_label = "PR増加量"
    axis = ["plain", "sci"]
    # save_path = "../../../Picture/距離とPR増加量/{}_{}.png" # グラフ名_ノードID_重み
    
    # 実装部分
    for graph_name in graph_list:
        title = graph_name
        graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
        x_list, y_list = return_list_1(graph, weight)
        make_plt(x_list, y_list, figsize=figsize, x_label=x_label, y_label=y_label, title=title, axis=axis)

# パターン 2 の実行関数
def main_2():
    # ハイパーパラメータ
    graph_list = ["com"]
    # graph_list = ["amazon0601"]
    weight = 2 # RW開始数の重み
    
    # グラフ描画用設定
    figsize = (6, 6)
    x_label = "重み付けしたノードからの距離"
    y_label = "PR増加量"
    title = "距離とPR増加量"
    axis = ["plain", "sci"]
    save_path = "../../../Picture/距離とPR増加量/{}_{}.png" # グラフ名_ノードID_重み
    
    # 実装部分
    for graph_name in graph_list:
        graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
        x_list, y_list = return_list_2(graph, weight)
        make_plt(x_list, y_list, figsize=figsize, x_label=x_label, y_label=y_label, title=title, axis=axis, save_path=save_path.format(graph_name, weight))

# パターン 3 の実行関数
def main_3():
    # ハイパーパラメータ
    graph_list = ["com"]
    # graph_list = ["amazon0601"]
    weight = 2 # RW開始数の重み
    
    # グラフ描画用設定
    figsize = (6, 6)
    x_label = "重み付けしたノードからの距離"
    y_label = "PR増加率"
    axis = ["plain", "sci"]
    # save_path = "../../../Picture/距離とPR増加量/{}_{}.png" # グラフ名_ノードID_重み
    
    # 実装部分
    for graph_name in graph_list:
        title = graph_name
        graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
        x_list, y_list = return_list_3(graph, weight)
        make_plt(x_list, y_list, figsize=figsize, x_label=x_label, y_label=y_label, title=title, axis=axis)

if __name__ == "__main__":
    # main_1()
    # main_2()
    main_3()