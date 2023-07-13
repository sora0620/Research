import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import Calc

DIV_NUM = 10
# graph : "web-Google", "amazon0601", "p2p-Gnutella24", "soc-Epinions1", "scale_free", "wiki-Talk"
GRAPH = "wiki-Talk"
PARTITION = "NXMETIS"
NUM = 0
ORIGIN_FLAG = False # True -> ORIGIN, False -> PARTITION

def disp_dist(flag):
    if flag == True:
        fig, ax = plt.subplots()
        
        graph = Calc.read_origin_graph(GRAPH)

        ax.set_xlabel("In_Deg")
        ax.set_ylabel("Ratio")
        ax.set_xticks(np.arange(11))
        ax.set_yticks(np.arange(0, 1.1, 0.1))
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("In Deg Dist")
        dist = Calc.in_degree_dist(graph)
        ax.scatter(dist[0], dist[1], s=10, color="blue")
        
        plt.show()
        
    elif flag == False:
        fig, ax = plt.subplots()
        
        subgraph_list = Calc.read_partition_graph(DIV_NUM, PARTITION, GRAPH, NUM)

        ax_list = []

        for i in range(DIV_NUM):
            ax_list.append(fig.add_subplot(2, 5, i+1))

        for i in range(DIV_NUM):
            ax_list[i].set_xlabel("In_Deg")
            ax_list[i].set_ylabel("Ratio")
            ax_list[i].set_xticks(np.arange(11))
            ax_list[i].set_yticks(np.arange(0, 1.1, 0.1))
            ax_list[i].set_xscale("log")
            ax_list[i].set_yscale("log")
            ax_list[i].set_title(f"In Deg Dist_{i}")
            dist = Calc.in_degree_dist(subgraph_list[i])
            ax_list[i].scatter(dist[0], dist[1], s=10, color="blue")
            
        plt.show()

disp_dist(ORIGIN_FLAG)