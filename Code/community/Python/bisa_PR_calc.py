import networkx as nx
import random

FILE_NAME = "../../../Dataset/Origin/{}.adjlist"

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
    関数の簡潔な説明をここに書きます。

    Parameters:
        graph (DiGraph): 対象グラフ
        bias_rate (float): ノード数を指定するための割合
        rw_weight (int): 偏らせるノードから開始するRWerの数 (ノードの重み)

    Returns:
        return_type: 偏らせたPR結果 (辞書型)
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
    
    return pr
        
def main():
    # ハイパーパラメータ
    graph_list = ["amazon0601"]
    rw_weight = 2 # RW開始数の重み
    bias_rate = 0.01 # PRを偏らせるノード数を決定するための割合
    
    for graph_name in graph_list:
        graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
        print("グラフの読み込み..., 完了！")
        print(bias_pr(graph, bias_rate, rw_weight))
    
if __name__ == "__main__":
    main()