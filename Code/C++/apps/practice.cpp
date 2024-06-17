#include <iostream>
#include <vector>
#include <cmath>
#include <utility>
#include <limits>
#include <chrono>
#include "../include/graph.h"
#include "../include/calc.h"
#include "../include/util.hpp"

// g++ -std=c++17 practice.cpp graph.cpp calc.cpp

using namespace std;

int main() {
    StdRandNumGenerator gen;

    string graph_name = "soc-Epinions1";
    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();
    vector<int> sample_vec;
    int weight_node_num = 100;
    int random_walk_num = (int) (pow(10, 6) / weight_node_num); // pow 関数は引数と戻り値が double 型なので, 計算時にキャスト変換する必要無し
    unordered_map<int, vector<int>> adj_map = origin_graph.get_adjacency_list();

    gen.gen_sample(node_vec, sample_vec, weight_node_num);
    cout << sample_vec.size() << endl;

    auto start = chrono::system_clock::now();
    for (int node : sample_vec) {
        unordered_map<int, double> ppr = origin_graph.calc_ppr_by_fora(node, random_walk_num);
        // unordered_map<int, double> ppr = personalized_pagerank(adj_map, node_vec, node, random_walk_num);
    }
    auto end = chrono::system_clock::now();
    auto dur = end - start;
    double microsec = chrono::duration_cast<chrono::microseconds>(dur).count();
    double time = microsec / pow(10, 6); // マイクロ秒を秒に変換
    cout << "Time: " << time << endl;
}