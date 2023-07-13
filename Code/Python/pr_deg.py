import networkx as nx
import Calc

# 元グラフのPR上位 UPPER_NUM ノードは, それぞれどの部分グラフにあたるノード集合に含まれているのかを調べる
# 例えば 10 分割したとき, 元グラフの上位 100 ノードが綺麗に 10 個ずつ各部分グラフに含まれていれば良いが, そうじゃない場合も存在するはず
# どういう要因によって偏りが発生するかを調べる必要がある
# ここでは, とりあえず部分グラフ内の合計次数との関係性を見てみる

READ_TRUE_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/true_edge.adjlist"
READ_REP_FILE =  "../../Dataset/Partition/div_{}/{}/{}/num_{}/origin/part_{}/cut_edge.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/origin/part_0.adjlist"
SAVE_SAMPLED_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/sampling/part_{}.adjlist"
# 例 :       "./data/partition_data/div_30/BFS/amazon0601/num_0/size_0.1/FF/ver_0/sampling/part_0.adjlist"
SAVE_SYNTHESIS_FILE = "../../Dataset/Partition/div_{}/{}/{}/num_{}/size_{}/{}/ver_{}/synthesis.adjlist"
EXCEL_NAME = "../../Excel/pr_deg.xlsx"
UPPER_NUM = 100 # 上位何位までを見るか

def excel_value(div, graph, partition):
    if graph == "p2p-Gnutella24":
        row = 2 + 5 * 0
    elif graph == "scale_free":
        row = 2 + 5 * 1
    elif graph == "wiki-Talk":
        row = 2 + 5 * 2
    elif graph == "web-Google":
        row = 2 + 5 * 3
    elif graph == "soc-Epinions1":
        row = 2 + 5 * 4
    elif graph == "amazon0601":
        row = 2 + 5 * 5
    
    if partition == "RN":
        column = 3 + (div + 2) * 0
    elif partition == "BFS":
        column = 3 + (div + 2) * 1
    elif partition == "NXMETIS":
        column = 3 + (div + 2) * 2
    elif partition == "BISECTION":
        column = 3 + (div + 2) * 3 

    return column, row

def pr_deg(div, partition, graph, num):
    origin_graph = Calc.read_origin_graph(graph)
    subgraph_list = Calc.read_partition_graph(div, partition, graph, num)
    cut_edge_graph_list = Calc.read_cut_edge_graph(div, partition, graph, num)

    # PR 部分
    pr_origin = nx.pagerank(origin_graph)
    pr_sorted = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
    subgraph_node_list = []
    where_is_upper_node = [0] * div # PR 上位 UPPER_NUM 個のノードがそれぞれどの部分グラフに存在するか
    
    for subgraph in subgraph_list:
        subgraph_node_list.append(set(list(subgraph)))
    
    for i in range(UPPER_NUM):
        current_node = pr_sorted[i][0]
        
        for j, node_list in enumerate(subgraph_node_list):
            if current_node in node_list:
                where_is_upper_node[j] += 1
    
    # 次数部分
    edge_num_list = []
    
    for subgraph in subgraph_list:
        edge_num_list.append(len(list(subgraph.edges())))
    
    edge_sum = sum(edge_num_list)
    
    for i in range(len(edge_num_list)):
        edge_num_list[i] /= edge_sum
    
    # カットエッジ本数部分
    cut_num_list = []
    
    for subgraph in cut_edge_graph_list:
        cut_num_list.append(len(list(subgraph.edges())))
    
    edge_sum = sum(cut_num_list)
    
    for i in range(len(cut_num_list)):
        cut_num_list[i] /= edge_sum
    
    sheet_name = "div_{}".format(div)
    column, row = excel_value(div, graph, partition)
    for i in range(div):
        Calc.write_excel(where_is_upper_node[i], EXCEL_NAME, sheet_name, column=column+i, row=row)
        Calc.write_excel(edge_num_list[i], EXCEL_NAME, sheet_name, column=column+i, row=row+1)
        Calc.write_excel(cut_num_list[i], EXCEL_NAME, sheet_name, column=column+i, row=row+2)


div_list = [2, 10]
partition_list = ["RN", "BFS", "NXMETIS", "BISECTION"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0]

for div in div_list:
    for partition in partition_list:
        for graph in graph_list:
            for num in num_list:
                pr_deg(div, partition, graph, num)