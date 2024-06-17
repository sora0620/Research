#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <filesystem>
#include <utility>
#include <algorithm>
#include <chrono>
#include <map>
#include "../include/graph.h"
#include "../include/read.h"

// Files to compile
// g++ -std=c++20 pagerank.cpp graph.cpp

using namespace std;

int main(int argc, char* argv[]) {
    /* グラフ選択 */
    string graph_name;
    cout << "Enter graph name : ";
    cin >> graph_name;

    /* グラフのデータセットがあるか確認 */
    string graph_path = "../../../Dataset/Origin/Graph/" + graph_name + ".adjlist";
    if(!filesystem::is_regular_file(graph_path)){ // なければ異常終了
        cout << "There are no such datasets" << endl;
        return 1;
    }

    /* グラフ読み込み */
    Graph graph(graph_path);
    cout << "Compleate reading graph" << endl;

    int N = graph.get_number_of_nodes();
    int E = graph.get_number_of_edges();

    cout << "Nodes : " << N << endl;
    cout << "Edges : " << E << endl;

    auto start = chrono::system_clock::now();

    unordered_map<int, double> score = graph.pagerank();

    auto end = chrono::system_clock::now();       // 計測終了時刻を保存
    auto dur = end - start;        // 要した時間を計算
    auto msec = chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    std::cout << "PageRank Calc Time: " << msec / float(1000) << " milli sec \n";

    cout << "Complete PageRank" << endl;

    // ノード番号ソート
    // map はキーの昇順で自動的にソートされるようになっている
    map<int, double> id_ordered_score;

    for (auto iter = score.begin(); iter != score.end(); iter++) {
        id_ordered_score[iter->first] = iter->second;
    }

    string pr_result_path = "./" + graph_name + "_pr.txt";
    ofstream ofs;
    ofs.open(pr_result_path);

    for (auto iter = id_ordered_score.begin(); iter != id_ordered_score.end(); iter++) {
        ofs << iter->first << " " << iter->second << endl;
    }

    return 0;
}