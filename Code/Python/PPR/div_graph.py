import networkx as nx
import Calc

USER_FILE = "../../Dataset/Partition/user/{}.adjlist"
PROVIDER_FILE = "../../Dataset/Partition/provider/{}.adjlist"
USER_TO_PROVIDER_FILE =  "../../Dataset/Partition/user_to_provider/{}.txt"
PROVIDER_TO_USER_FILE = "../../Dataset/Partition/provider_to_user/{}.txt"

# 無向グラフ読み込み
def read_undirected_graph(graph_name):
    file_name = "../../Dataset/Origin/{}.adjlist"
    origin_graph = nx.read_adjlist(file_name.format(graph_name), nodetype=int, create_using=nx.Graph)
    
    print("Reading Completed! : {}".format(graph_name))
    
    return origin_graph

# 有向グラフ読み込み
def read_directed_graph(graph_name):
    file_name = "../../Dataset/Origin/{}.adjlist"
    origin_graph = nx.read_adjlist(file_name.format(graph_name), nodetype=int, create_using=nx.DiGraph)
    
    print("Reading Completed! : {}".format(graph_name))
    
    return origin_graph

# 二分割したグラフの両方を有向グラフとして返す
def return_div_graph(undirected_graph, directed_graph):
    div_node_taple = nx.community.kernighan_lin_bisection(undirected_graph)
    graph_list = []
    
    for node_set in div_node_taple:
        tmp_graph = directed_graph.subgraph(list(node_set))
        graph_list.append(tmp_graph)
    
    return graph_list

def return_border_edge(origin_graph, user_graph, provider_graph):
    edge_set = set(list(origin_graph.edges()))
    user_edge_set = set(list(user_graph.edges()))
    provider_edge_set = set(list(provider_graph.edges()))
    
    user_node_set = set(list(user_graph))
    
    border_edge_set = edge_set - (user_edge_set | provider_edge_set)
    
    user_to_proveder = []
    provider_to_user = []
    
    for edge in border_edge_set:
        source_node = edge[0]
        if source_node in user_node_set:
            user_to_proveder.append(edge)
        else:
            provider_to_user.append(edge)
    
    return user_to_proveder, provider_to_user

# エッジリスト形式でデータとして保存
def write_in_txt_graph(edge_list, filename):
    with open(filename, 'w') as f:
        for edge in edge_list:
            write_edge = '{} {}\n'.format(edge[0], edge[1])
            f.write(write_edge)

def main():
    # ハイパーパラメータ
    graph_name = "soc-Epinions1"
    origin_graph = read_directed_graph(graph_name)
    undirected_graph = read_undirected_graph(graph_name)
    div_graph_list = return_div_graph(undirected_graph, origin_graph)
    
    user_graph = div_graph_list[0]
    provider_graph = div_graph_list[1]
    
    Calc.write_in_adjlist(user_graph, USER_FILE.format(graph_name))
    Calc.write_in_adjlist(provider_graph, PROVIDER_FILE.format(graph_name))
    user_to_provider, provider_to_user = return_border_edge(origin_graph, user_graph, provider_graph)
    write_in_txt_graph(user_to_provider, USER_TO_PROVIDER_FILE.format(graph_name))
    write_in_txt_graph(provider_to_user, PROVIDER_TO_USER_FILE.format(graph_name))
    
if __name__ == "__main__":
    main()