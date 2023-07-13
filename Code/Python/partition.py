import networkx as nx
import Calc
import time

# データを隣接情報として保存するパターン

# 定数
SIZE_RANGE = 0.2 # グラフサイズを縮小する際、書く部分グラフのノード数の範囲をどこまで許すかを決めるパラメータ
READ_FILE = "../../Dataset/Origin/Graph/{}.adjlist"
TRUE_EDGE_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/true_edge.adjlist" # 部分グラフ内のエッジ
CUT_EDGE_FILE =  "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/cut_edge.adjlist"  # 分割の際にカットされたエッジの複製情報
INFORMATION_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/information.txt"
GRAPH_NUM = 3 # グラフ分割に生じるランダム性を考慮して, 複数回分割を行い, それを全て残しておく

# 各分割手法を利用した際の、分割グラフ(DiGraph)をリストで返す
def select_partition_method(graph, partition, div):
    if partition == "BFS":
        return Calc.make_subgraph_BFS(graph, div, SIZE_RANGE)
    elif partition == "NXMETIS":
        return Calc.make_subgraph_NXMETIS(graph, div)
    elif partition == "BISECTION":
        return Calc.make_subgraph_BISECTION(graph, div)
    elif partition == "RN":
        return Calc.make_subgraph_RN(graph, div, SIZE_RANGE)

# 各部分グラフにおける複製情報を、グラフとして返す
def cut_edge_graph(origin_graph, subgraph_list):
    cut_graph_list = [] # 各部分グラフの複製情報のみからなるグラフを格納
    
    for subgraph in subgraph_list:
        cut_graph = nx.DiGraph() # 複製されたエッジのみから構成されるグラフ
        node_set = set(list(subgraph))
        
        for node in node_set:
            # 出隣接ノードの場合
            out_node_adj = list(origin_graph.successors(node))
            for out_node in out_node_adj:
                if out_node not in node_set:
                    cut_graph.add_edge(node, out_node)
            
            # 入隣接ノードの場合
            in_node_adj = list(origin_graph.predecessors(node))
            for in_node in in_node_adj:
                if in_node not in node_set:
                    cut_graph.add_edge(in_node, node)
        
        cut_graph_list.append(cut_graph)
    
    return cut_graph_list

# ハイパーパラメータ
div_list = [2, 10]
graph_name = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
partition_list = ["RN", "BISECTION", "NXMETIS", "BFS"]

# 変数設定
graph_list = [] # 元グラフのリスト

# コード領域
for name in graph_name:
    read_graph = nx.read_adjlist(READ_FILE.format(name), nodetype=int, create_using=nx.DiGraph)
    graph_list.append(read_graph)

for div in div_list:
    for partition in partition_list:
        for i, name in enumerate(graph_name):
            for k in range(GRAPH_NUM):
                
                print(div, "分割, ", "{}, ".format(partition), name, k, "回目")
                tim_start = time.perf_counter()
                
                subgraph_list = select_partition_method(graph_list[i], partition, div)
                cut_graph_list = cut_edge_graph(graph_list[i], subgraph_list)
                
                tim_end = time.perf_counter()
                tim = tim_end - tim_start
                print("Partition Time :", tim)
                
                file_name = []
                for j in range(div):
                    # 分割グラフを保存
                    f_true_edge = TRUE_EDGE_FILE.format(div, partition, name, k, j)
                    Calc.write_in_adjlist(subgraph_list[j], f_true_edge)
                    
                    # 複製情報を保存
                    f_cut_edge = CUT_EDGE_FILE.format(div, partition, name, k, j)
                    Calc.write_in_adjlist(cut_graph_list[j], f_cut_edge)
                    
                with open(INFORMATION_FILE.format(div, partition, name, k), "w") as f:
                    for j in range(div):
                        nodes = len(list(subgraph_list[j]))
                        edges = len(list(subgraph_list[j].edges()))
                        cut_edge_num = len(list(cut_graph_list[j].edges()))
                        f.write(f"No.{j}, nodes : {nodes}, edges : {edges}\n")
                        f.write(f"          cut : {cut_edge_num}")
                        
                if partition == "NXMETIS":
                    break