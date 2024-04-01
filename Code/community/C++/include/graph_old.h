#ifndef GUARD_GRAPH_H
#define GUARD_GRAPH_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <time.h>
#include <map>
#include <fstream>
#include <string>
#include <sstream>
#include "../include/graph.h"

using namespace std;

class Graph
{
    private: // グラフをコンストラクタを使用して作成したら, とりあえずこれらは作成するような関数にする
        unordered_set<int> node_list_set;
        unordered_map<int, vector <int> > adjacency_list; // ノードid -> 隣接ノードの set
        unordered_map<int, unordered_set <int> > in_neighbor_list;
        unordered_map<int, int> degree;

    public:
        // デフォルトコンストラクタ
        Graph();

        // ファイル名を引数に取ると, そのファイルを読み込んだグラフを作成
        Graph(string file_path);

        // サンプリング等で取得したノードセットが存在し, 元グラフのエッジ関係を利用してグラフを作成したい場合
        Graph(unordered_set<int> node_set, Graph origin_graph);

        // 全ノードが格納された vector を, ノードの昇順に並べて返す
        const vector<int> get_node_list_id_sort();

        // 全ノードが格納された set を返す
        const unordered_set<int> get_node_set();

        // const 参照の隣接リストを返す
        const unordered_map<int, vector <int> > get_adjacency_list();

        // const 参照の入隣接リストを返す
        const unordered_map<int, unordered_set <int> > get_in_adj_list();

        // ノード数を返す
        const int get_number_of_nodes();

        // エッジ数を返す
        const int get_number_of_edges();

        // PR 値 unordered_map
        unordered_map<int, double> pr_list;

        // ノードの追加
        void add_node(int node);

        // エッジ追加　有向グラフ
        void add_edge(int n1, int n2);

        void add_adj_edge(unordered_map<int, unordered_set <int> > node_map);

        // エッジ追加 無向グラフ
        void u_add_edge(int n3, int n4);

        // ノード削除
        void remove_node(int node);

        // n1 -> n2 のエッジ削除
        void remove_edge(int n1, int n2);

        // pagerank 演算
        unordered_map<int, double> pagerank();
};

#endif // GURAD_GRAPH_H