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

void write_json(string graph_name, unordered_map<pair<int, int>, double, pairhash> edge_ppr_map)
{
    string path = "../../../Dataset/PPR/" + graph_name + "_edge_ppr.json";

    ofstream ofs(path);
    if (ofs.good())
    {
        json m_json;

        for (auto& [p, ppr] : edge_ppr_map) {
            string key = to_string(p.first) + " " + to_string(p.second);
            m_json[key] = ppr;
        }

        ofs << m_json.dump(4);
    }
    else
    {
        cout << "ファイルの読み込みに失敗しました" << endl;
    }
}

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    int random_walk_num = (int) pow(10, 6);
    int start_node = 0;

    Graph origin_graph(graph_name);
    
    unordered_map<pair<int, int>, double, pairhash> edge_ppr;
    vector<pair<int, int> > edge_vec = origin_graph.get_edge_vec();
    for (auto& [source_node, target_node] : edge_vec) {
        edge_ppr[make_pair(source_node, target_node)] = 0;
    }
    origin_graph.calc_edge_ppr_by_fora(edge_ppr, start_node, random_walk_num);

    // 正規化
    double sum = 0;
    for (auto& [source_node, target_node] : edge_vec) {
        sum += edge_ppr[make_pair(source_node, target_node)];
    }

    for (auto& [source_node, target_node] : edge_vec) {
        edge_ppr[make_pair(source_node, target_node)] /= sum;
    }

    write_json(graph_name, edge_ppr);

    return 0;
}