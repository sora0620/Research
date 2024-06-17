import networkx as nx
import Calc
import Sampling as sp
import random

def return_weight(origin_graph, connect_node_list, weight_range, default_weight):
    weight_dict = {node: default_weight for node in list(origin_graph)}
    for node in connect_node_list:
        weight_dict[node] = random.randint(default_weight+1, weight_range)
    
    return weight_dict

def return_sampling_graph(graph_name, graph, connect_node_list, sampling_rate, sampling_method, weight_dict, default_weight, weight_node_num, weight_range):
    sampling_graph = nx.DiGraph()
    if sampling_method == "RE":
        obj = sp.RE()
        sampling_graph = obj.random_edge_sampling(graph, sampling_rate)
    elif sampling_method == "FC":
        obj = sp.FC()
        sampling_graph = obj.flow_control_sampling(graph, sampling_rate, connect_node_list, weight_dict, default_weight)
    elif sampling_method == "FC_random":
        obj = sp.FC()
        sampling_graph = obj.fc_random_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_prefer_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "FC_top_prefer":
        obj = sp.FC()
        sampling_graph = obj.fc_top_prefer_sampling(graph, sampling_rate, weight_node_num, default_weight, weight_range)
    elif sampling_method == "BC_in_out":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_in_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "BC_in":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_in_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "BC_out":
        obj = sp.BC()
        sampling_graph = obj.betweenness_centrality_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "EBC":
        obj = sp.EBC()
        sampling_graph = obj.edge_betweenness_centraliry_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_in_out":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_in_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_in":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_in_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "CC_out":
        obj = sp.CC()
        sampling_graph = obj.closeness_centrality_out_sampling(graph, graph_name, sampling_rate)
    elif sampling_method == "PR_in_out":
        obj = sp.PR()
        sampling_graph = obj.pagerank_in_out_sampling(graph, sampling_rate)
    elif sampling_method == "PR_in":
        obj = sp.PR()
        sampling_graph = obj.pagerank_in_sampling(graph, sampling_rate)
    elif sampling_method == "PR_out":
        obj = sp.PR()
        sampling_graph = obj.pagerank_out_sampling(graph, sampling_rate)
    elif sampling_method == "EPR":
        obj = sp.EPR()
        sampling_graph = obj.edge_pagerank_sampling(graph, sampling_rate)
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

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    sampling = "FC"
    border = "prefer" # 境界ノードの選択方法
    sampling_num = 10 # データとして保存しておく回数
    weight_node_num = 100
    weight_range = 100 # 境界ノードの重み幅
    default_weight = 50 # 基本の重み
    # rate_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    rate_list = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    
    origin_graph = Calc.read_origin_graph(graph_name)
    
    for i in range(sampling_num):
        connect_node_list = []
        if border == "random":
            connect_node_list = Calc.select_border_node(origin_graph, weight_node_num) # ランダム選択
        elif border == "prefer":
            connect_node_list = Calc.select_border_prefer(origin_graph, weight_node_num) # 優先付着
        weight_dict = return_weight(origin_graph, connect_node_list, weight_range, default_weight)
        
        for rate in rate_list:
            path = "../../../Sampling_Data/FC_{}/{}/ver_{}.adjlist".format(border, str(rate), i+1)
            sampling_graph = return_sampling_graph(graph_name, origin_graph, connect_node_list, rate, sampling, weight_dict, default_weight, weight_node_num, weight_range)
            Calc.write_in_adjlist(sampling_graph, path)
    
if __name__ == "__main__":
    main()