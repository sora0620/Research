import Calc
import networkx as nx

def return_ppr(graph, start_node):
    weight_dict = {node: 0 for node in list(graph)}
    weight_dict[start_node] = 1
    
    ppr_dict = nx.pagerank(graph, personalization=weight_dict)
    
    return ppr_dict

def main():
    # ハイパーパラメータ
    graph_name = "twitter"
    border_type = "prefer"
    border_num_list = [50, 100, 500] # 境界ノード数
    loop_num = 3 # 何回分取得するか
    
    graph = Calc.read_origin_graph(graph_name)
    
    for border_num in border_num_list:
        for i in range(loop_num):
            j = 1
            connect_node_list = Calc.read_connect_list(graph_name, border_type, border_num, i)
            print(connect_node_list)
            for node in connect_node_list:
                print(f"境界ノード数 {border_num}, ver_{i}, {j}個目")
                path = "../../../Dataset/Centrality/PPR/{}/{}.json".format(graph_name, node)
                ppr_dict = return_ppr(graph, node)
                Calc.write_in_json(ppr_dict, path)
                j += 1

if __name__ == "__main__":
    main()