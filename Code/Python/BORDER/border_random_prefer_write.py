import networkx as nx
import Sampling as sp
import random
import Calc
import json
import numpy as np

def return_weight(origin_graph, connect_node_list, weight_range, default_weight):
    personalization_dict = {node: default_weight for node in list(origin_graph)}
    for node in connect_node_list:
        personalization_dict[node] = random.randint(default_weight+1, weight_range)
    
    return personalization_dict

def return_sampling_graph(graph, connect_node_list, sampling_rate, sampling_method, personalization_dict, default_weight, ppr_dict):
    sampling_graph = nx.DiGraph()
    
    if sampling_method == "FC":
        obj = sp.FC()
        sampling_graph = obj.flow_control_sampling_2(graph, sampling_rate, connect_node_list, personalization_dict, default_weight, ppr_dict)
    else:
        print("Sampling Error!")
        exit(1)
    
    # 境界ノードとその周辺の出エッジが取得されないと困るので、取得されていない場合は必ずサンプリング割合分だけ取得されるように設定
    for node in connect_node_list:
        if node not in set(list(sampling_graph)):
            sampling_graph.add_node(node)
        out_edge_list = list(graph.successors(node))
        if sampling_graph.out_degree(node) == 0 and len(out_edge_list) != 0:            
            get_out_num = int(len(out_edge_list) * sampling_rate)
            if get_out_num == 0:
                get_out_num = 1
            
            tmp_list = random.sample(out_edge_list, get_out_num)
            for out_node in tmp_list:
                sampling_graph.add_edge(node, out_node)
    
    return sampling_graph

def update_json(graph, path):
    edge_dict = {}
    
    with open(path, 'r') as f:
        edge_dict = json.load(f)
    
    edge_dict["sampling_num"] += 1
    edge_list = list(graph.edges())
    
    for source_node, target_node in edge_list:
        key = f"{source_node} {target_node}"
        edge_dict[key] += 1
        
    with open(path, "w") as f:
        json.dump(edge_dict, f, indent=4)

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    path = "../../../Dataset/Sampling_Edge/{}_prefer.txt".format(graph_name)
    sampling = "FC"
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    sampling_rate = 0.2 # サンプリングサイズ
    loop_num = 100 # 何回サンプリングを行うか
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_list = list(origin_graph)
    deg_list = []
    
    sum = 0
    for node in node_list:
        deg = origin_graph.in_degree(node)
        deg_list.append(deg)
        sum += deg
        
    for i in range(len(node_list)):
        deg_list[i] /= sum
        
    for _ in range(loop_num):
        connect_node_list = np.random.choice(node_list, size=weight_node_num, p=deg_list, replace=False)
        personalization_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
        
        # 任意の１ノードを起点とした PPR 辞書を取得
        def get_ppr(source_node):
            ppr_weight = {node: 0 for node in node_list}
            ppr_weight[source_node] = 1
            
            ppr_dict = nx.pagerank(origin_graph, personalization=ppr_weight)
            
            return ppr_dict
        
        ppr_dict = {}
        for node in connect_node_list:
            ppr_dict[node] = get_ppr(node)
        
        sampling_graph = return_sampling_graph(origin_graph, connect_node_list, sampling_rate, sampling, personalization_dict, default_weight, ppr_dict)
        update_json(sampling_graph, path)

if __name__ == "__main__":
    main()