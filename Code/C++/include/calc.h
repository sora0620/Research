#ifndef GUARD_CALC_H
#define GUARD_CALC_H

#include <vector>
#include <unordered_map>

using namespace std;
class Graph;

unordered_map<int, double> pagerank(Graph& graph);

unordered_map<int, double> personalized_pagerank(unordered_map<int, vector<int>>& adj_map, vector<int>& node_vec, int start_node, int random_walk_num);

#endif // GUARD_CALC_H