#include <string>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <iostream>
#include "../include/graph.h"
#include "../include/json.hpp"
#include "../include/calc.h"
#include "../include/pair_hash.hpp"

using namespace std;
using json = nlohmann::json;

// g++ -std=c++17 return_edge_ppr.cpp graph.cpp calc.cpp

void write_json(string graph_name, unordered_map<int, unordered_map <int, double> >& edge_ppr_map, vector<pair<int, int> >& edge_vec)
{
    string path = "../../../Dataset/Centrality/edge_ppr.json";

    ofstream ofs(path);
    if (ofs.good())
    {
        json m_json;

        for (auto& [source_node, target_node] : edge_vec) {
            string key = to_string(source_node) + " " + to_string(target_node);
            m_json[key] = edge_ppr_map[source_node][target_node];
        }

        ofs << m_json.dump(4);
    }
    else
    {
        cout << "ファイルの読み込みに失敗しました" << endl;
    }
}

// int main(int argc, char* argv[])
// {
//     // ハイパーパラメータ
//     string graph_name = "soc-Epinions1";
//     int random_walk_num = (int) pow(10, 6);
//     int start_node = 0;

//     Graph origin_graph(graph_name);
    
//     unordered_map<int, unordered_map <int, double> > edge_ppr;
//     vector<pair<int, int> > edge_vec = origin_graph.get_edge_vec();

//     for (auto& [source_node, target_node] : edge_vec) {
//         edge_ppr[source_node][target_node] = 0;
//     }

//     origin_graph.calc_edge_ppr_by_fora(edge_ppr, start_node, random_walk_num);

//     // 正規化
//     double sum = 0;
//     for (auto& [source_node, target_node] : edge_vec) {
//         sum += edge_ppr[source_node][target_node];
//     }

//     for (auto& [source_node, target_node] : edge_vec) {
//         edge_ppr[source_node][target_node] /= sum;
//     }

//     double print_sum = 0;
//     for (auto& [source_node, target_node] : edge_vec) {
//         print_sum += edge_ppr[source_node][target_node];
//     }

//     write_json(graph_name, edge_ppr, edge_vec);

//     return 0;
// }

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    int random_walk_num = (int) pow(10, 6);
    int start_node = 0;

    Graph origin_graph(graph_name);
    
    unordered_map<int, unordered_map <int, double> > edge_ppr;
    vector<pair<int, int> > edge_vec = origin_graph.get_edge_vec();
    
    unordered_map<int, double> ppr = origin_graph.calc_ppr_by_fora(start_node, random_walk_num);

    for (auto& [source_node, target_node] : edge_vec) {
        edge_ppr[source_node][target_node] = ppr[source_node] / origin_graph.get_degree(source_node);
    }

    write_json(graph_name, edge_ppr, edge_vec);

    return 0;
}