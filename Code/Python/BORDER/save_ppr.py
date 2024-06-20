import Calc
import networkx as nx

def return_ppr(graph, start_node):
    weight_dict = {node: 0 for node in list(graph)}
    weight_dict[start_node] = 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    
    return ppr_dict

def main():
    # ハイパーパラメータ
    graph_name = "slashdot"
    border_type = "prefer"
    border_num_list = [50, 100, 500] # 境界ノード数
    loop_num = 3 # 何回分取得するか
    loop_ver = 2 # 0 or 1 or 2
    
    graph = Calc.read_origin_graph(graph_name)
    calc_node_set = set()
    
    # 全ノードに対して行う
    # for border_num in border_num_list:
    #     for i in range(loop_num):
    #         connect_node_list = Calc.read_connect_list(graph_name, border_type, border_num, i)
    #         calc_node_set.update(set(connect_node_list))
    
    # for i, node in enumerate(calc_node_set):
    #     path = "../../../Dataset/Centrality/PPR/{}/{}.json".format(graph_name, node)
    #     print(f"{i+1} / {len(calc_node_set)}")
    #     ppr_dict = return_ppr(graph, node)
    #     Calc.write_in_json(ppr_dict, path)
    
    # １つのノードに対して行う (複数のターミナルで動かして擬似的に並列化した方が早い)   
    for border_num in border_num_list:
        connect_node_list = Calc.read_connect_list(graph_name, border_type, border_num, loop_ver)
        calc_node_set.update(set(connect_node_list))
    
    for i, node in enumerate(calc_node_set):
        path = "../../../Dataset/Centrality/PPR/{}/{}.json".format(graph_name, node)
        print(f"{i+1} / {len(calc_node_set)}")
        ppr_dict = return_ppr(graph, node)
        Calc.write_in_json(ppr_dict, path)

if __name__ == "__main__":
    main()