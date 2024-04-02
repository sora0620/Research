import networkx as nx
import random
import japanize_matplotlib
import matplotlib.pyplot as plt
import math

FILE_NAME = "../../../Dataset/Origin/{}.adjlist"
COM_FILE = "../../../Dataset/Partition/div_{}/{}/sub_{}.adjlist"

# ランダムにPRを偏らせて, それらがコミュニティ内のPRにどういう結果を与えるかを比較
# 境界ノードはランダム選択
    # 全体の１％
# RWを増やす開始ノード数はノード数全体の内, １％としよう
# 一旦, RW開始数は２倍にしてみよう

def random_node_select(graph, random_node_num):
    """
    ランダムに選択したPRを偏らせるノードのリストを返す.

    Parameters:
        graph (DiGraph): 対象のグラフ
        random_node_num (int): 選択するノード数

    Returns:
        return_type: ノードのリスト
    """
    
    node_list = list(graph)
    select_node = random.sample(node_list, random_node_num)
    
    return select_node

def bias_pr(graph, bias_rate, rw_weight):
    """
    ノードに重み付けをしてPRを偏らせた際のPR計算結果を返す

    Parameters:
        graph (DiGraph): 対象グラフ
        bias_rate (float): ノード数を指定するための割合
        rw_weight (int): 偏らせるノードから開始するRWerの数 (ノードの重み)

    Returns:
        pr (dict): 偏らせたPR結果
    """

    bias_dict = {}
    node_list = []
    node_num = len(list(graph))
    random_node_num = int(node_num * bias_rate)
    
    if random_node_num == 0:
        random_node_num = 1
    
    bias_node_list = random_node_select(graph, random_node_num)
    
    for node in node_list:
        bias_dict[node] = 1
    
    for node in bias_node_list:
        bias_dict[node] = rw_weight
    
    pr = nx.pagerank(graph, personalization=bias_dict)
    
    print("重み付け PR の計算..., 完了！")
    
    return pr

def return_community_node_list(graph_name, com_num):
    """
    各コミュニティ内のノードのリストを返す

    Parameters:
        graph_name (string): グラフ名
        com_num (int): コミュニティ数

    Returns:
        return_list (list): 各コミュニティに存在するノード ID を, リストの入れ子で返す. なお, リストの格納順番は "com_0" から昇順
    """
    
    return_list = []
    
    for i in range(com_num):
        path = COM_FILE.format(com_num, graph_name, i)
        tmp_graph = nx.read_adjlist(path, nodetype=int, create_using=nx.DiGraph)
        print(f"com_{i} 読み込み..., 完了！")
        tmp_list = list(tmp_graph)
        return_list.append(tmp_list)
    
    return return_list

def return_com_pr_list(graph_name, bias_rate, rw_weight, com_num):
    """
    plt で表示するために, 各ノードに対応させた PR を返す.
    x は元の PR, y は重み付け後の PR.
    各コミュニティ毎に結果を表示したいため, コミュニティ毎にリストを作成し, それを更にリストに格納した.

    Parameters:
        graph_name (string): グラフの名称
        bias_rate (float): ノード数を指定するための割合
        rw_weight (int): 偏らせるノードから開始するRWerの数 (ノードの重み)
        com_num (int): コミュニティの個数

    Returns:
        return_x_list, return_y_list (list の list): 各ノードに対応させた PR の値を, 各コミュニティ毎にリストで格納したリスト
    """
    
    return_x_list = []
    return_y_list = []
    com_node_list = []
    
    graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
    print("グラフの読み込み..., 完了！")
    
    normal_pr_dict = nx.pagerank(graph)
    bias_pr_dict = bias_pr(graph, bias_rate, rw_weight)
    com_node_list = return_community_node_list(graph_name, com_num)
    
    for i in range(com_num):
        node_list = com_node_list[i]
        tmp_x_list = []
        tmp_y_list = []
        for node in node_list:
            tmp_x_list.append(normal_pr_dict[node])
            tmp_y_list.append(bias_pr_dict[node])
        return_x_list.append(tmp_x_list)
        return_y_list.append(tmp_y_list)
    
    return return_x_list, return_y_list

def make_plt(x_list_list, y_list_list, figsize=(10, 10), main_title=None, subtitle_list=None, x_label=None, y_label=None, save_path=None):
    """
    複数のグラフを表示するための関数
    左上から右下に向かって順番に描画
    
    Parameters:
        x_list_list, y_list_list (listのlist): 表示したいデータ群を, 各々リストに格納 (各インデックスが対応)
        figsize (taple): グラフ全体のサイズ
        main_title (string): グラフ全体のタイトル
        subtitle_list (list (string)): 各グラフのタイトルをリストに格納
        x_label (string): 横軸の名前
        y_label (string): 縦軸の名前
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
        tmp_ax.scatter(x_list_list[i], y_list_list[i])

    # plt の設定
    if save_path != None:
        plt.savefig(save_path)
    if main_title != None:
        plt.title(main_title)
    plt.tight_layout()
    plt.show()
    plt.close()

def main():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    rw_weight = 2 # RW開始数の重み
    bias_rate = 0.01 # PRを偏らせるノード数を決定するための割合
    com_num = 3 # コミュニティ数
    
    # グラフ描画用設定
    figsize = (10, 10)
    main_title = "重み付けPR計算における, 各コミュニティ内でのPR値変化"
    subtitle_list = []
    for i in range(com_num):
        subtitle_list.append(f"com_{i}")
    x_label = "一般のPR値"
    y_label = "重み付けPR値"
    save_path = "../../../Picture/重み付けPR/お試し.png"
    
    # 実装部分
    for graph_name in graph_list:
        x_list_list, y_list_list = return_com_pr_list(graph_name, bias_rate, rw_weight, com_num)
        make_plt(x_list_list, y_list_list, figsize=figsize, main_title=main_title, subtitle_list=subtitle_list, x_label=x_label, y_label=y_label, save_path=save_path)

if __name__ == "__main__":
    main()