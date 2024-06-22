import networkx as nx
import Calc

def main():
    # ハイパーパラメータ
    graph_name = "twitter"
    cent_type = "CC"
    save_path = f"../../../Dataset/Centrality/{cent_type}/{graph_name}.json"
    div_num = 10 # 媒介中心性を計算する精度
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_num = origin_graph.number_of_nodes()
    cent_dict = {}
    
    if cent_type == "BC":
        cent_dict = nx.betweenness_centrality(origin_graph, k=int(node_num / div_num))
    elif cent_type == "CC":
        cent_dict = nx.closeness_centrality(origin_graph)
    
    Calc.write_in_json(cent_dict, save_path)

if __name__ == "__main__":
    main()