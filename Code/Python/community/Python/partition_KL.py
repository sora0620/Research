import networkx as nx
from networkx.algorithms.community import kernighan_lin_bisection
import matplotlib.pyplot as plt
import Calc
import itertools

# KL法 (kernighan_lin_bisection) で分割
# KL法自体は無向グラフにしか適用できないっぽいんだけど, girvan_newman もそうっぽいのでまあしゃあなしで実行速度が速いしこれをつかおうという流れになりました
# 最後に有向に戻すのを忘れずに

READ_FILE = "../../../Dataset/Origin/{}.adjlist"
WRITE_FILE =  "../../../Dataset/Partition/div_{}/{}/sub_{}.adjlist"

def find_max_array_index(arr):
    """
    ノード数が最大のサブグラフの番号(インデックス)を返す関数

    Parameters:
    arr: 各サブグラフのノードのセットを格納したtaple

    Returns:
    max_index: ノード数が最大のサブグラフの番号(インデックス)
    """
    
    max_length = 0
    max_index = -1
    
    for i in range(len(arr)):
        if len(arr[i]) > max_length:
            max_length = len(arr[i])
            max_index = i
    
    return max_index

def graph_partition(graph_name, community_size):
    """
    グラフを subgraph_size 個に分割する関数
    分割方法は, KL法を使用
    KL法は2分割手法のため, 常に最大のノード数を持つグラフに対して分割を実行
    最後に, 分割した有向グラフを返す
    有向, 無向の使い分けに注意

    Parameters:
    graph (Graph) : グラフを格納
    community_size (int) : 分けたいコミュニティの個数を定義

    Returns:
    community_list: 分割後の各グラフをリストに格納して返す
    """
    
    undirected_graph = nx.read_adjlist(READ_FILE.format(graph_name), nodetype=int, create_using=nx.Graph) # 無向グラフ, 分割自体はこちらで行う
    directed_graph = nx.read_adjlist(READ_FILE.format(graph_name), nodetype=int, create_using=nx.DiGraph) # 有向グラフ, 最後に返すのはこちらを使用
    print("Graph Read Completed!")
    
    subgraph_list = [] # 分割後のグラフを格納
    subgraph_node_list = [] # 分割後のサブグラフのノードをセット型で格納
    div_graph = undirected_graph # 分割対象のグラフ
    
    for i in range(community_size-1):
        bisection_node_taple = kernighan_lin_bisection(div_graph) # ({グラフ１のノードセット}, {グラフ２のノードセット}) という形の返り値となる
        for node_set in bisection_node_taple:
            subgraph_node_list.append(list(node_set))
        
        # 分割が最後じゃない場合のみ, 次の分割対象を探す
        if i != community_size-2:
            node_max_subgraph_id = find_max_array_index(subgraph_node_list)
            node_list = subgraph_node_list.pop(node_max_subgraph_id)
            div_graph = undirected_graph.subgraph(node_list)
    
    for subgraph_nodes in subgraph_node_list:
        subgraph_list.append(directed_graph.subgraph(subgraph_nodes))
    
    return subgraph_list

def write_graph(graph_name, subgraph_list):
    community_size = len(subgraph_list)
    
    for i, subgraph in enumerate(subgraph_list):
        path = WRITE_FILE.format(community_size, graph_name, i)
        Calc.write_in_adjlist(subgraph, path)

def main():
    # ハイパーパラメータ
    # graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "twitter"]
    graph_list = ["com"]
    community_size = 3
    
    # 実行関数
    for graph_name in graph_list:
        subgraph_list = graph_partition(graph_name, community_size)
        write_graph(graph_name, subgraph_list)
    
if __name__ == "__main__":
    main()