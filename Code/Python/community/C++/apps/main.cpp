#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <filesystem>
#include <utility>
#include <bits/stdc++.h> // iota
#include <time.h> // time
#include "../include/graph.h"
#include "../include/read.h"

// Files to compile
// g++ main.cpp graph.cpp read.cpp -std=gnu++17

using namespace std;
namespace fs = filesystem;

int main(int argc, char* argv[]){

    /* グラフ選択 */
    string graph_name;
    cout << "Enter graph name : ";
    cin >> graph_name;

    /* グラフのデータセットがあるか確認 */
    //string dataset_path = "../datasets/original/" + graph_name + ".txt"; //original データセット
    string dataset_path = "../datasets/Gorder/" + graph_name + "_Gorder.txt"; //Gorder されたデータセット
    if(!fs::is_regular_file(dataset_path)){ // なければ異常終了
        cout << "There are no such datasets" << endl;
        return 1;
    }

    /* グラフ読み込み */
    Graph graph;
    read_graph_from_text_file(dataset_path, graph);
    cout << "Compleate reading graph" << endl;

    /* グラフ情報(ノード数, エッジ数) */
    int N = graph.get_number_of_nodes();
    int E = graph.get_number_of_edges();

    cout << "Nodes : " << N << endl;
    cout << "Edges : " << E << endl;


    /* PR値読み込み */
    string pr_path = "../pr_result/" + graph_name + "/" + graph_name + "_Gorder_pr.txt"; 
    if(!fs::is_regular_file(pr_path)){ // なければ異常終了
        cout << "There are no such PR results" << endl;
        return 1;
    }

    read_pr_from_text_file(pr_path, graph);
    cout << "Compleate reading PR" << endl;

    cout << "PR List Size : " << graph.pr_list.size() << endl;

    /* 頂点IDをブロック化 */
    double alpha = 0.01 / 100; // ブロックサイズ 0.01%
    //cout << "Enter Block Size : ";
    //cin >> alpha;

    // 跨ぎなしのブロック
    //vector<vector<int>> block = graph.get_block(alpha); 

    // 跨ぎありのブロック
    vector<vector<int>> block = graph.get_cross_block(alpha);

    
    int block_num = block.size(); // ブロック数
    cout << "Block Num : " << block_num << endl;

    /* ブロックスコアを計算 */
    vector<double> block_score = graph.get_block_score(block, graph.pr_list);



    // ブロックスコアをソート 昇順(小さい順)
    vector<int> index(block_score.size());
    iota(index.begin(), index.end(), 0);
    sort(index.begin(), index.end(), [&](int x, int y){return block_score[x] < block_score[y];});

    cout << "End Sort" << endl;
    //cout << block_score[index[0]] << endl;

    /* ブロックサンプリング */

    // サンプリング率
    double sampling_rate;
    cout << "Sampling Rate : ";
    cin >> sampling_rate;

    // 上位ブロック取得割合
    double beta = 0.1;
    //cout << "Enter beta : ";
    //cin >> beta;

    unordered_set<int> sampling_nodes = graph.block_sampling(block_num, block, index,
    sampling_rate, beta);

    cout << "End Block Sampling" << endl;

    cout << "Sampling Size : " << sampling_nodes.size() << endl;

    
    /* サンプリングしたノードを txt ファイルに出力 */
    string nodes_file;
    cout << "Enter Nodes file name : ";
    cin >> nodes_file;

    string nodes_path = "../sampling_datasets/" + graph_name + "/" + nodes_file + ".txt";
    ofstream ofs;
    ofs.open(nodes_path);

    for(auto& id : sampling_nodes){
        ofs << id << endl;
    }
    

    return 0;
}

