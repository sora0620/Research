import networkx as nx
import Calc

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    save_path = f"../../../Dataset/BC/{graph_name}_edge.json"
    div_num = 10 # 媒介中心性を計算する精度
    
    origin_graph = Calc.read_origin_graph(graph_name)
    node_num = origin_graph.number_of_nodes()
    # エッジ媒介中心性計算
    bc_dict = nx.edge_betweenness_centrality(origin_graph, k=int(node_num / div_num))
    write_bc = {}
    
    for edge, bc in bc_dict.items():
        key = f"{edge[0]} {edge[1]}"
        write_bc[key] = bc
    
    Calc.write_in_json(write_bc, save_path)

if __name__ == "__main__":
    main()