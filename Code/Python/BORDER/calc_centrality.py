import networkx as nx
import Calc

def main_bc():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    save_path = f"../../../Dataset/BC/{graph_name}.json"
    div_num = 10 # 媒介中心性を計算する精度
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_num = origin_graph.number_of_nodes()
    bc_dict = nx.betweenness_centrality(origin_graph, k=int(node_num / div_num))
    Calc.write_in_json(bc_dict, save_path)

def main_cc():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    save_path = f"../../../Dataset/CC/{graph_name}.json"
    
    origin_graph = Calc.read_origin_graph(graph_name)
    cc_dict = nx.closeness_centrality(origin_graph)
    Calc.write_in_json(cc_dict, save_path)

if __name__ == "__main__":
    main_cc()