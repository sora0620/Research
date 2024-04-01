#include <string>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <vector>
#include "../include/graph.h"

using namespace std;

// グラフ file_path で指定したファイルに adjlist 型で記述
void write_to_file(string file_path, Graph graph)
{
    ofstream write_file(file_path);
    if (!write_file) {
        cerr << file_path << " を開けませんでした。" << endl;
    }

    map<int, set <int> > ordered_adj_list;
    unordered_set<int> node_set = graph.get_node_set();
    unordered_map<int, unordered_set <int> > adjacency_list = graph.get_adjacency_list();

    for (auto iter = adjacency_list.begin(); iter != adjacency_list.end(); iter++) {
        for (int neighbor_node : iter->second) {
            ordered_adj_list[iter->first].insert(neighbor_node);
        }
    }

    // 要素を持たない map は, size() で確認するとそのキーを持つ箱は存在しているが, iteration で回すと飛ばして読み込まれるため
    // iter->first でソースノードを参照することができなくなってしまうらしい！注意！
    set<int> ordered_node_set;

    for (int node : node_set) {
        ordered_node_set.insert(node);
    }

    for (int node : ordered_node_set) {
        write_file << node << " ";
        for (int neighbor_node : ordered_adj_list[node]) {
            write_file << neighbor_node << " ";
        }
        write_file << endl;
    }

    write_file.close();

    return;
}