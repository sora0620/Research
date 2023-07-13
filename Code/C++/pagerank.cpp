#include "header.h"
#include "MyGraph.h"
#include "useful.h"

#define ALPHA 0.85
#define MAX_ITER 100

std::map<int, double> pagerank(MyGraph G)
{
    const int error = G.number_of_nodes * std::pow(10, -6);
    
    std::map<int, double> node_pr;
    double sink_pr = (1 - ALPHA) / (double) G.number_of_nodes;

    for (int node : G.node_vec) {
        node_pr[node] = 1 / (double) G.number_of_nodes;
    }

    for (int node : G.node_vec) {
        if (G.out_neighbor_map[node].size() == 0) {
            G.out_neighbor_map[node] = G.node_vec;
            for (int neighbor_node : G.node_vec) {
                G.in_neighbor_map[neighbor_node].push_back(node);
            }
        }
    }

    for (int i = 0; i < MAX_ITER; i++) {
        std::map<int, double> tmp_map;

        for (int node : G.node_vec) {
            double pr_in_sum = 0;

            for (int neighbor_node : G.in_neighbor_map[node]) {
                pr_in_sum += node_pr[neighbor_node] / (double) G.out_neighbor_map[neighbor_node].size();
            }

            tmp_map[node] = sink_pr + ALPHA * pr_in_sum;
        }

        double error_sum = 0;

        for (int node : G.node_vec) {
            error_sum += abs(node_pr[node] - tmp_map[node]);
        }

        if (error_sum < error) {
            break;
        }

        node_pr = tmp_map;
    }
    
    return node_pr;
}

int main()
{
    std::string file_name = "../../Dataset/Origin/Graph/p2p-Gnutella24.adjlist";

    MyGraph G(file_name);

    std::map<int, double> node_pr = pagerank(G);

    print(node_pr);

    return 0;
}