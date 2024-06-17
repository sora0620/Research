#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <iostream>
#include "../include/graph.h"
#include "../include/json.hpp"
#include "../include/calc.h"

using namespace std;
using json = nlohmann::json;

// g++ -std=c++17 return_multi_source_ppr.cpp graph.cpp calc.cpp

void write_json(string graph_name, unordered_map<int, double> ppr_map)
{
    string path = "../../../Dataset/PPR/" + graph_name + "_multi_ppr.json";

    ofstream ofs(path);
    if (ofs.good())
    {
        json m_json;

        for (auto [node, ppr] : ppr_map) {
            m_json[to_string(node)] = ppr;
        }

        ofs << m_json.dump(4);
    }
    else
    {
        cout << "ファイルの読み込みに失敗しました" << endl;
    }
}

unordered_map<int, double> return_multi_source_ppr_map(Graph& graph, vector<int>& connect_node_vec, unordered_map<int, int> weight_map, int random_walk_num)
{
    unordered_map<int, double> mulit_souce_ppr_map;
    unordered_map<int, vector<int> > adj_map = graph.get_adjacency_list();
    vector<int> node_vec = graph.get_node_vec();

    for (int node : node_vec) {
        mulit_souce_ppr_map[node] = 0;
    }

    double tmp_sum = 0;

    for (int start_node : connect_node_vec) {
        unordered_map<int, double> tmp_ppr_origin = personalized_pagerank(adj_map, node_vec, start_node, random_walk_num);
        // unordered_map<int, double> tmp_ppr_origin = graph.calc_ppr_by_fora(start_node, random_walk_num);

        for (int node : node_vec) {
            double add_value = tmp_ppr_origin[node] * weight_map[start_node];
            mulit_souce_ppr_map[node] += add_value;
            tmp_sum += add_value;
        }
    }

    for (auto [node, ppr] : mulit_souce_ppr_map) {
        mulit_souce_ppr_map[node] /= tmp_sum;
    }

    return mulit_souce_ppr_map;
}

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    vector<int> start_node_vec;
    for (int i = 0; i < 10; i++) {
        start_node_vec.push_back(i);
    }
    int random_walk_num = (int) (pow(10, 6) / start_node_vec.size());

    unordered_map<int, int> weight_map;
    for (int i = 0; i < 10; i++) {
        weight_map[i] = i + 1;
    }

    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();
    unordered_map<int, double> ppr_map = return_multi_source_ppr_map(origin_graph, start_node_vec, weight_map, random_walk_num);
    write_json(graph_name, ppr_map);

    return 0;
}