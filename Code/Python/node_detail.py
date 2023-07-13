import networkx as nx
import Calc

SIZE_RATE = 0.001
FILE_NAME = "../../Dataset/Partition/div_{}/{}/{}/num_{}/detail/part_{}.txt"

def return_node_detail(div, partition, graph, num):
    origin_graph = Calc.read_origin_graph(graph)
    partition_graph_list = Calc.read_partition_graph(div, partition, graph, num)
    
    pr_origin = nx.pagerank(origin_graph)
    sorted_pr_origin = sorted(pr_origin.items(), key=lambda x:x[1], reverse=True)
    
    compare_num = int(len(list(origin_graph)) * SIZE_RATE)
    
    origin_node_rank_dict = {} # 元グラフのノードを key, PR 順位を NDCG の比較範囲 (上位 0.1 %) 分のランキングを value.
    i = 1
    
    for k, v in sorted_pr_origin[:compare_num]:
        origin_node_rank_dict[k] = i
        i += 1

    for i, partition_graph in enumerate(partition_graph_list):
        node_set = set(list(partition_graph))
        
        pr_partition = nx.pagerank(partition_graph)
        sorted_pr_partition = sorted(pr_partition.items(), key=lambda x:x[1], reverse=True)
        
        partition_node_ranking = {} # 部分グラフのノードを key, PR 順位を value.
        j = 1
        
        for k, v in sorted_pr_partition:
            partition_node_ranking[k] = j
            j += 1
        
        node_detail = {} # key: ノード, value: {"o_rank": 元グラフでのランキング, "o_in": , "o_out": , "p_rank": partition内でのランキング, "p_in": , "pout": }
        
        for node in origin_node_rank_dict.keys():
            if node in node_set:
                node_detail[node] = {"o_rank": origin_node_rank_dict[node], 
                                     "o_in": len(list(origin_graph.predecessors(node))), 
                                     "o_out": len(list(origin_graph.successors(node))),
                                     "p_rank": partition_node_ranking[node],
                                     "p_in": len(list(partition_graph.predecessors(node))),
                                     "p_out": len(list(partition_graph.successors(node)))}

        with open(FILE_NAME.format(div, partition, graph, num, i), "w") as f:
            f.write("  node o_rank o_in o_out p_rank p_in p_out\n")
            
            for node, pr in sorted_pr_origin[:compare_num]:
                if node in node_detail:
                    d = node_detail[node]
                    f.write("{:>6} {:>6} {:>4} {:>5} {:>6} {:>4} {:>5}\n".format(node, d["o_rank"], d["o_in"], d["o_out"], d["p_rank"], d["p_in"], d["p_out"]))

div_list = [2, 10]
partition_list = ["BFS", "BISECTION", "NXMETIS"]
graph_list = ["p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601"]
num_list = [0, 1, 2]

for div in div_list:
    for partition in partition_list:
        for graph in graph_list:
            if partition == "NXMETIS":
                tmp_num = [0]
            else:
                tmp_num = num_list
            for num in tmp_num:
                return_node_detail(div, partition, graph, num)