import networkx as nx
import matplotlib.pyplot as plt
import Calc

FILE_NAME = "../../../Dataset/Origin/{}.adjlist"

# グラフ自体を描画

def disp(graph_name):
    graph = nx.read_adjlist(FILE_NAME.format(graph_name), nodetype=int, create_using=nx.DiGraph)
    nx.draw(graph, node_size=100, width=1)
    plt.show()

def main():
    # ハイパーパラメータ
    graph_list = ["com"]

    for graph in graph_list:
        disp(graph)
                    
if __name__ == "__main__":
    main()