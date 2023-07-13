import networkx as nx
import random
import Calc

READ_FILE = "./graph/{}.adjlist"
SAVE_FILE = "./data/partition_data/origin_graph/{}.adjlist"

SIZE = 100000 # ノード数を選択

def graph_scaling(graph, size):
    origin_graph = nx.read_adjlist(READ_FILE.format(graph), nodetype=int, create_using=nx.DiGraph)
    scaling_graph = nx.DiGraph()
    node_list = list(origin_graph)

    while len(list(scaling_graph)) != size:
        initial_node = random.choice(node_list)
        scaling_graph.add_node(initial_node)
        node_list.remove(initial_node)
        
        for edge in list(nx.dfs_edges(origin_graph, initial_node)):
            print(len(list(scaling_graph)))
            if len(list(scaling_graph)) == size:
                break
            ad_node = edge[1]
            scaling_graph.add_node(ad_node)
            if ad_node in node_list:
                node_list.remove(ad_node)

    node_list = list(scaling_graph)
    for current_node in node_list:
        for adjacency_node in list(origin_graph.successors(current_node)):
            if adjacency_node in node_list:
                scaling_graph.add_edge(current_node, adjacency_node)

    Calc.write_in_adjlist(scaling_graph, SAVE_FILE.format(graph))
    
graph_list = ["Stanford", "wiki-Talk", "NotreDame"]

for graph in graph_list:
    graph_scaling(graph, SIZE)