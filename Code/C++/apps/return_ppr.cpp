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

// g++ -std=c++17 return_ppr.cpp graph.cpp calc.cpp

void write_json(string graph_name, unordered_map<int, double> ppr_map)
{
    string path = "../../../Dataset/PPR/" + graph_name + "_ppr.json";

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

int main(int argc, char* argv[])
{
    // ハイパーパラメータ
    string graph_name = "soc-Epinions1";
    int random_walk_num = (int) pow(10, 6);
    int start_node = 0;

    Graph origin_graph(graph_name);
    vector<int> node_vec = origin_graph.get_node_vec();
    unordered_map<int, vector <int> > adj_map = origin_graph.get_adjacency_list();
    
    // unordered_map<int, double> ppr_map = personalized_pagerank(adj_map, node_vec, start_node, random_walk_num);
    unordered_map<int, double> ppr_map = origin_graph.calc_ppr_by_fora(start_node, random_walk_num);
    write_json(graph_name, ppr_map);

    return 0;
}