import networkx as nx
import matplotlib.pyplot as plt
import Calc

# グラフ自体を描画

def disp(graph):
    G = Calc.read_origin_graph(graph)
    nx.draw(G, node_size=100, width=1)
    plt.show()

def main():
    # ハイパーパラメータ
    graph_list = ["practice_2"]

    for graph in graph_list:
        disp(graph)
                    
if __name__ == "__main__":
    main()