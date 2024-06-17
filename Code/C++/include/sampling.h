#ifndef GUARD_SAMPLING_H
#define GUARD_SAMPLING_H

#include <vector>
#include <unordered_map>

using namespace std;
class Graph;

Graph Simple_Random_Walk(Graph& complete_graph, double rate);

Graph Forest_Fire(Graph& complete_graph, int nodes_to_sample);

// FORA 導入前
// Graph Flow_Control(Graph& origin_graph, double rate, vector<int> connect_node_vec, unordered_map<int, int> border_weight_dict, int default_weight, unordered_map<int, unordered_map<int, double> > ppr_dict);

// FORA 導入 (& PPR 計算の中に他のエッジ PPR 計算も含めて高速化したやつ) 導入後
Graph Flow_Control(Graph& origin_graph, double rate, vector<int> connect_node_vec, vector<int> rwer_flow_vec, int default_weight, int random_walk_num);

Graph Random_Edge(Graph& origin_graph, double rate);

#endif // GUARD_SAMPLING_H