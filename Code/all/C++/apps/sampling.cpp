#include <unordered_map>
#include <vector>
#include <fstream>
#include <filesystem>
#include <utility>
#include <time.h> // time
#include <unordered_set>
#include <iostream>
#include <string>
#include <iterator>
#include <random>
#include <algorithm>
#include <format>
#include <queue>
#include "../include/graph.h"
#include "../include/read.h"
#include "../include/write.h"

using namespace std;
namespace fs = filesystem;

// g++ -std=c++20 sampling.cpp graph.cpp read.cpp write.cpp

// unordered_map 型の変数を value にてソートするための関数
// reverse が true だと降順, false だと昇順でソート
template<typename T,typename U>
vector<pair <T, U> > sort_second(unordered_map<T, U> origin_map, bool reverse)
{
    vector<pair <T, U> > sorted_vec;
    vector<pair <U, T> > tmp_vec;

    for (auto iter = origin_map.begin(); iter != origin_map.end(); iter++) {
        pair<U, T> tmp_pair = make_pair(iter->second, iter->first);
        tmp_vec.push_back(tmp_pair);
    }
    if (reverse == true) {
        sort(tmp_vec.rbegin(), tmp_vec.rend());
    } else if (reverse == false) {
        sort(tmp_vec.begin(), tmp_vec.end());
    }

    for (pair<U, T> p : tmp_vec) {
        pair<T, U> tmp_pair = make_pair(p.second, p.first);
        sorted_vec.push_back(tmp_pair);
    }

    return sorted_vec;
}

// vector<pair <T, U> > 型の変数を pair の 2 つめの変数にてソートするための関数
// reverse が true だと降順, false だと昇順でソート
template<typename T,typename U>
vector<pair <T, U> > sort_second(vector<pair <T, U> > origin_vec, bool reverse)
{
    vector<pair <T, U> > sorted_vec;
    vector<pair <U, T> > tmp_vec;

    for (pair p : origin_vec) {
        pair<U, T> tmp_pair = make_pair(p.second, p.first);
        tmp_vec.push_back(tmp_pair);
    }
    if (reverse == true) {
        sort(tmp_vec.rbegin(), tmp_vec.rend());
    } else if (reverse == false) {
        sort(tmp_vec.begin(), tmp_vec.end());
    }

    for (pair<U, T> p : tmp_vec) {
        pair<T, U> tmp_pair = make_pair(p.second, p.first);
        sorted_vec.push_back(tmp_pair);
    }

    return sorted_vec;
}

/*
Graph random_edge(Graph G, int nodes_to_sample)
{
    auto start = chrono::system_clock::now();

    // 乱数生成
    std::random_device seed_gen;
    std::mt19937 engine {seed_gen()};

    // サンプリングしたグラフを入れる箱. これを return する.
    Graph sampling_graph;

    // ノードのリスト
    unordered_set<int> node_list = G.get_node_set();

    // グラフの隣接リスト
    unordered_map<int, vector <int> > adjacency_list = G.get_adjacency_list();
    
    // エッジの全ペアを [source_node, target_node] としてsetに格納する変数
    unordered_set<vector <int> > edge_set;

    // edge_set に全エッジを格納
    for (auto iter = adjacency_list.begin(); iter != adjacency_list.end(); iter++) {
        for (int i = 0; i < iter->second.size(); i++) {
            vector<int> tmp_vec;
            tmp_vec.push_back(iter->first);
            tmp_vec.push_back(iter->second.at(i));
            edge_set.insert(tmp_vec);
        }
    }
    
    // 確認用
    int flag = 0;

    // ここからサンプリング開始
    while (sampling_graph.get_number_of_nodes() != nodes_to_sample) {
        if (edge_set.size() != 0) {

            // 取得エッジをランダムに選択
            vector<int> selected_edge;
            sample(edge_set.begin(),
                   edge_set.end(),
                   std::back_inserter(selected_edge),
                   1,
                   engine);

            // 最後の 1 エッジの選択方法
            if ((nodes_to_sample - sampling_graph.get_number_of_nodes()) == 1) {
                unordered_set<int> check_node = sampling_graph.get_node_set();

                // エッジの両端がまだサンプリンググラフに追加されていない場合
                if (check_node.find(selected_edge[0]) == check_node.end() && 
                    check_node.find(selected_edge[1]) == check_node.end()) {
                        sampling_graph.add_node(selected_edge[0]);

                // エッジのどちらか or 両端のノードが既にサンプリンググラフに追加されている場合
                } else {
                    sampling_graph.add_edge(selected_edge[0], selected_edge[1]);
                }
            
            // 基本はここでエッジ & ノード追加
            } else {
                sampling_graph.add_edge(selected_edge.at(0), selected_edge.at(1));
            }
            
            // 一度取得したエッジは次回以降の候補から外す
            edge_set.erase(selected_edge);
        
        // 選択可能なエッジが無くなった場合. ノードをそのまま追加
        } else {
            flag++;

            if (flag == 1) {
                cout << "選択可能なエッジが無くなりました" << endl;
            }

            int selected_node;
            sample(node_list.begin(),
                   node_list.end(),
                   std::back_inserter(selected_node),
                   1,
                   engine);
            sampling_graph.add_node(selected_node);
            node_list.erase(selected_node);
        }
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    std::cout << "RE_Time: " << msec / float(1000) << " milli sec \n";
    
    return sampling_graph;
}
*/

Graph Simple_Random_Walk(Graph complete_graph, int nodes_to_sample)
{
    auto start = chrono::system_clock::now();

    // 乱数生成
    std::random_device seed_gen;
    std::mt19937 engine {seed_gen()};

    int growth_size = 2;
    int T = 100;    // number of iterations
    int iteration = 1;
    int edges_before_t_iter = 0;
    Graph sampled_graph;

    unordered_set<int> node_set = complete_graph.get_node_set();
    unordered_map<int, unordered_set <int> > in_adj_map = complete_graph.get_in_adj_list();
    unordered_map<int, unordered_set <int> > out_adj_map = complete_graph.get_adjacency_list();
    vector<int> node_vec;

    sample(node_set.begin(),
        node_set.end(),
        back_inserter(node_vec),
        1,
        engine);
    
    int current_node = node_vec.at(0);
    node_set.erase(current_node);
    sampled_graph.add_node(current_node);

    while (sampled_graph.get_number_of_nodes() < nodes_to_sample) {        
        if (sampled_graph.get_number_of_nodes() == nodes_to_sample) {
            break;
        }

        unordered_set<int> edges = out_adj_map[current_node];
        if (edges.size() != 0) {
            node_vec.clear();
            sample(edges.begin(),
                edges.end(),
                back_inserter(node_vec),
                1,
                engine);
            int chosen_node = node_vec.at(0);
            sampled_graph.add_edge(current_node, chosen_node);
            current_node = chosen_node;
            node_set.erase(current_node);
        }

        iteration++;

        if (iteration % T == 0) {
            if (sampled_graph.get_number_of_edges() - edges_before_t_iter < growth_size) {
                node_vec.clear();
                sample(node_set.begin(),
                    node_set.end(),
                    std::back_inserter(node_vec),
                    1,
                    engine);
                current_node = node_vec.at(0);
                node_set.erase(current_node);
                sampled_graph.add_node(current_node);
            }
            edges_before_t_iter = sampled_graph.get_number_of_edges();
        }
    }

    if (sampled_graph.get_number_of_nodes() > nodes_to_sample) {
        cerr << "Over Node Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    std::cout << "SRW_Time: " << msec / float(1000) << "sec\n";
    
    return sampled_graph;
}

Graph Forest_Fire(Graph complete_graph, int nodes_to_sample)
{
    auto start = chrono::system_clock::now();

    // 乱数生成
    std::random_device seed_gen;
    std::mt19937 engine {seed_gen()};

    double forward_prob = 0.7, back_prob = 0.2; // 前方燃焼確率と後方燃焼確率
    vector<int> node_vec; // シードノード用
    queue<int> que; // キュー
    int initial_node; // FF の開始ノード
    int random_node;
    Graph sampled_graph; // サンプリンググラフ
    unordered_map<int, int> flag; // 一度取得したノードは 2 度操作はしない. 2 度してしまうと, 2 回隣接取得を行うことになり FF の意味がない
    unordered_set<int> node_set = complete_graph.get_node_set(); // 元グラフのノードリスト
    unordered_map<int, unordered_set <int> > out_adj_list = complete_graph.get_adjacency_list(); // 出隣接ノード
    unordered_map<int, unordered_set <int> > in_adj_list = complete_graph.get_in_adj_list(); // 入隣接ノード

    // ノード取得の有無を初期化
    for (int node : node_set) {
        flag[node] = 0;
    }

    node_vec.clear();
    sample(node_set.begin(),
        node_set.end(),
        back_inserter(node_vec),
        1,
        engine);
    random_node = node_vec.at(0); // シードノードを取得
    
    que.push(random_node); // シードノードをプッシュ
    sampled_graph.add_node(random_node); // 隣接が存在しない場合もあるため, シードノードをサンプリンググラフに追加
    node_set.erase(random_node);

    while (sampled_graph.get_number_of_nodes() != nodes_to_sample) {
        // キューにノードが存在する場合
        if (que.size() > 0) {
            initial_node = que.front(); // 開始ノードを取得
            node_set.erase(initial_node);
            que.pop(); // キューから削除

            // 開始ノードがまだ隣接取得を行ったことがない場合
            if (flag[initial_node] == 0) {
                if (sampled_graph.get_number_of_nodes() == nodes_to_sample) {
                    break;
                }
                // sampled_graph.add_node(initial_node);
                unordered_set<int> out_neighbors = out_adj_list[initial_node];
                unordered_set<int> in_neighbors = in_adj_list[initial_node];

                  // 成功確率0.7の事象をsize回試行する
                binomial_distribution<> out_dist(out_neighbors.size(), forward_prob);
                // 成功した回数を取得(0以上out_neighbors.size()以下の値が返される)
                int out_num = out_dist(engine);

                  // 成功確率0.2の事象をsize回試行する
                binomial_distribution<> in_dist(in_neighbors.size(), back_prob);
                // 成功した回数を取得(0以上in_neighbors.size()以下の値が返される)
                int in_num = in_dist(engine);

                vector<int> select_out_list;
                vector<int> select_in_list;

                sample(out_neighbors.begin(),
                    out_neighbors.end(),
                    back_inserter(select_out_list),
                    out_num,
                    engine);
                sample(in_neighbors.begin(),
                    in_neighbors.end(),
                    back_inserter(select_in_list),
                    in_num,
                    engine);
                
                for (int out_node : select_out_list) {
                    if (sampled_graph.get_number_of_nodes() == nodes_to_sample) {
                        break;
                    }
                    que.push(out_node);
                    sampled_graph.add_edge(initial_node, out_node);
                }

                for (int in_node : select_in_list) {
                    if (sampled_graph.get_number_of_nodes() == nodes_to_sample) {
                        break;
                    }
                    que.push(in_node);
                    sampled_graph.add_edge(in_node, initial_node);
                }
                flag[initial_node] = 1; // initial_node を隣接取得済みにする
            }

        // キューにノードが存在しない場合
        } else {
            node_vec.clear();
            sample(node_set.begin(),
                node_set.end(),
                back_inserter(node_vec),
                1,
                engine);
            random_node = node_vec.at(0); // シードノードを選択し直す
            que.push(random_node); // シードノードをプッシュ
            sampled_graph.add_node(random_node); // 隣接が存在しない場合もあるため, シードノードをサンプリンググラフに追加
            node_set.erase(random_node);
        }

        if (node_set.size() == 0) {
            cerr << "Error!" << endl;
            exit(1);
        }
    }

    if (sampled_graph.get_number_of_nodes() > nodes_to_sample) {
        cerr << "Over Node Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    std::cout << "FF_Time: " << msec / float(1000) << "sec\n";
    
    return sampled_graph;
}

/*
Graph Rank_Degree(Graph complete_graph, int nodes_to_sample, double ratio_of_seeds, double top_k_ratio)
{
    // 乱数生成
    std::random_device seed_gen;
    std::mt19937 engine {seed_gen()};

    Graph sampled_graph;
    int number_of_seeds = (int) ratio_of_seeds * complete_graph.get_number_of_nodes();
    if (number_of_seeds == 0) {
        cerr << "Seed_Error!" << endl;
        exit(1);
    }

    unordered_set<int> seed_set;
    unordered_set<int> node_set = complete_graph.get_node_set();
    Graph copy_graph = complete_graph;
    unordered_map<int, unordered_set <int> > copy_out_adj = copy_graph.get_adjacency_list();
    vector<int> random_vec;
    vector<int> deg_node_list;

    for (int node : copy_graph.get_node_set()) {
        if (copy_out_adj[node].size() != 0) {
            deg_node_list.push_back(node);
        }
    }

    if (deg_node_list.size() == 0) {
        random_vec.clear();
        sample(node_set.begin(),
            node_set.end(),
            back_inserter(random_vec),
            nodes_to_sample,
            engine);
        for (int node : random_vec) {
            sampled_graph.add_node(node);
        }
    } else {
        if (deg_node_list.size() < number_of_seeds) {
            seed_set.clear();
            for (int node : deg_node_list) {
                seed_set.insert(node);
            }
        } else {
            random_vec.clear();
            sample(deg_node_list.begin(),
                deg_node_list.end(),
                back_inserter(random_vec),
                number_of_seeds,
                engine);
            for (int node : random_vec) {
                seed_set.insert(node);
            }
        }
        for (int node : seed_set) {
            sampled_graph.add_node(node);
        }

        int flag = 0;

        while (true) {
            unordered_set<int> new_seed_set;
            unordered_set<pair <int, int> > add_edge_set;

            for (int current_node : seed_set) {
                vector<pair <int, int> > neighbor_deg;

                for (int neighbor_node : copy_out_adj[current_node]) {
                    neighbor_deg.push_back(make_pair(neighbor_node, copy_out_adj[neighbor_node].size()));
                }

                vector<pair <int, int> > deg_rank = sort_second(neighbor_deg, true);

                int number_of_top_nodes = top_k_ratio * neighbor_deg.size();

                if (number_of_top_nodes == 0) {
                    number_of_top_nodes = 1;
                }

                vector<int> tmp_list;
                for (int i = 0; i < number_of_top_nodes; i++) {
                    tmp_list.push_back(deg_rank.at(i).first);
                }

                for (int neighbor_node : tmp_list) {
                    new_seed_set.insert(neighbor_node);
                    pair<int, int> add_edge = make_pair(current_node, neighbor_node);
                    add_edge_set.insert(add_edge);
                }
            }

            for (pair<int, int> edge : add_edge_set) {
                sampled_graph.add_edge(edge.first, edge.second);
                copy_graph.remove_edge(edge.first, edge.second);

                if (sampled_graph.get_number_of_nodes() == nodes_to_sample) {
                    flag = 1;
                    break;
                } else if (sampled_graph.get_number_of_nodes() > nodes_to_sample) {
                    sampled_graph.remove_node(edge.second);
                    flag = 1;
                    break;
                }
            }

            if (flag == 1) {
                break;
            }
            // 90 行目まで写し完了
        }
    }

    return sampled_graph;
}
*/

Graph Top_PageRank_Neighbors(Graph complete_graph, int nodes_to_sample, unordered_map<int, double> pr_origin)
{
    auto start = chrono::system_clock::now();

    unordered_set<int> node_set;
    unordered_map<int, unordered_set <int> > neighbor_dict = complete_graph.get_in_adj_list();
    int rate = 1;
    int pr_rank = 0;

    vector<pair <int, double> > pr_sorted = sort_second(pr_origin, true);

    // ちゃんと PR の降順になっているかの確認用
    double bigger_pr = pr_sorted.at(0).second;
    for (pair<int, double> p : pr_sorted) {
        if (bigger_pr < p.second) {
            cerr << "Sort Error!" << endl;
            exit(1);
        }
        bigger_pr = p.second;
    }

    // 以下、サンプリング開始
    while (node_set.size() != nodes_to_sample) {
        int high_pr_node = pr_sorted.at(pr_rank).first;
        node_set.insert(high_pr_node);

        int neighbors_num = neighbor_dict[high_pr_node].size();
        unordered_map<int, double> neighbor_pr;
        
        for (int adj_node : neighbor_dict[high_pr_node]) {
            neighbor_pr[adj_node] = pr_origin[adj_node];
        }

        vector<pair <int, double> > neighbor_sorted = sort_second(neighbor_pr, true);
        neighbors_num *= rate;

        if (node_set.size() + neighbors_num <= nodes_to_sample) {
            for (int i = 0; i < neighbors_num; i++) {
                node_set.insert(neighbor_sorted.at(i).first);
            }
        } else {
            for (int i = 0; i < neighbors_num; i++) {
                if (node_set.size() == nodes_to_sample) {
                    break;
                }
                node_set.insert(neighbor_sorted.at(i).first);
            }
        }

        pr_rank++;
    }

    Graph sampled_graph(node_set, complete_graph);

    if (sampled_graph.get_number_of_nodes() > nodes_to_sample) {
        cerr << "Over Node Error!" << endl;
        exit(1);
    }

    auto end = chrono::system_clock::now();
    auto dur = end - start;
    auto msec = chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    // 要した時間をミリ秒（1/1000秒）に変換して表示
    std::cout << "TPN_Time: " << msec / float(1000) << "sec\n";

    return sampled_graph;
}

string size_define(Graph graph)
{
    int top_num = 100;
    unordered_map <int, unordered_set <int> > in_deg_map = graph.get_in_adj_list();
    unordered_map<int, double> pr_dict = graph.pagerank();
    vector<pair <int, double> > pr_sorted = sort_second(pr_dict, true);
    unordered_set<int> node_set;

    for (int i = 0; i < top_num; i++) {
        int top_node = pr_sorted[i].first;
        node_set.insert(top_node);

        for (int node : in_deg_map[top_node]) {
            node_set.insert(node);
        }
    }

    return to_string((double) node_set.size() / graph.get_number_of_nodes());
}

Graph return_sampling_graph(Graph origin_graph, string graph_name, string rate, string sampling)
{
    Graph sp_graph;
    float size;
    if (rate == "neighbor") {
        size = stof(size_define(origin_graph));
    } else {
        size = stof(rate);
    }

    auto now = chrono::system_clock::now();
    time_t end_time = chrono::system_clock::to_time_t(now);
    cout << "Sampling Start Time: " << ctime(&end_time);
 
    int graph_size = origin_graph.get_number_of_nodes() * size;

    // SRW
    if (sampling == "SRW") {
        sp_graph = Simple_Random_Walk(origin_graph, graph_size);
    // FF
    } else if (sampling == "FF") {
        sp_graph = Forest_Fire(origin_graph, graph_size);
    // TPN
    } else if (sampling == "TPN") {
        unordered_map<int, double> pr_origin = origin_graph.pagerank();
        sp_graph = Top_PageRank_Neighbors(origin_graph, graph_size, pr_origin);
    }

    cout << "Sampling Finished!" << endl;
    cout << "Nodes : " << sp_graph.get_number_of_nodes() << endl;
    cout << "Edges : " << sp_graph.get_number_of_edges() << endl;
    cout << endl;

    return sp_graph;
}

// 静的グラフの main 関数
int main(int argc, char* argv[])
{
    // vector<string> graph_list = {"p2p-Gnutella24", "scale_free", "wiki-Talk", "web-Google", "soc-Epinions1", "amazon0601", "wiki-Talk_origin", "twitter"};
    vector<string> graph_list = {"amazon0601"};
    vector<string> sampling_list = {"SRW", "FF", "TPN"};
    vector<int> ver_list = {0, 1, 2};
    vector<string> sampling_rate = {"0.05", "0.10", "0.20", "0.30", "neighbor"};
    vector<Graph> origin_graph_list;

    // グラフの読み込み
    for (string graph : graph_list) {
        cout << "Graph : " << graph << endl;
        string graph_path = "../../../Dataset/Static/Origin/" + graph + ".adjlist";
        if(!filesystem::is_regular_file(graph_path)){ // なければ異常終了
            cout << "There are no such datasets" << endl;
            return 1;
        }

        // グラフ読み込み
        Graph origin_graph(graph);
        origin_graph_list.push_back(origin_graph);
        cout << "Complete reading graph" << endl;

        int N = origin_graph.get_number_of_nodes();
        int E = origin_graph.get_number_of_edges();

        cout << "Nodes : " << N << endl;
        cout << "Edges : " << E << endl;
    }

    // ここまでは動いている

    for (int i = 0; i < graph_list.size(); i++) {
        for (string sampling : sampling_list) {
            vector<int> tmp_list;
            tmp_list.clear();
            if (sampling == "TPN") {
                tmp_list.push_back(0);
            } else {
                tmp_list = ver_list;
            }

            for (int ver : tmp_list) {
                for (string rate : sampling_rate) {
                    string size;
                    if (rate == "neighbor") {
                        size = size_define(origin_graph_list.at(i));
                    } else {
                        size = rate;
                    }

                    Graph sampling_graph = return_sampling_graph(origin_graph_list.at(i), graph_list.at(i), size, sampling);
                    if (sampling == "TPN") {
                        for (int j; j < ver_list.size(); j++) {
                            string path = "../../../Dataset/Static/Sampling/" + graph_list.at(i) + "/size_" + rate + "/" + sampling + "/ver_" + to_string(j) + "/sampling_graph.adjlist";
                            write_to_file(path, sampling_graph);
                        }
                    } else {
                        string path = "../../../Dataset/Static/Sampling/" + graph_list.at(i) + "/size_" + rate + "/" + sampling + "/ver_" + to_string(ver) + "/sampling_graph.adjlist";
                        write_to_file(path, sampling_graph);
                    }
                }
            }
        }
    }

    return 0;
}

// 動的グラフの main 関数
/*
int main(int argc, char* argv[])
{
    // vector<string> graph_list = {"stack", "slashdot", "facebook", "epinions", "email"};
    vector<string> graph_list = {"stack"};
    vector<string> sampling_list = {"SRW", "FF", "TPN"};
    vector<int> ver_list = {0, 1, 2};
    vector<string> sampling_rate = {"0.05", "0.10", "0.20", "0.30", "neighbor"};
    unordered_map<string, vector <Graph> > graph_map;
    int timestamp_num = 4;

    for (string name : graph_list) {
        vector<Graph> dynamic_vector;

        for (int i = 0; i < timestamp_num; i++) {
            string graph_path = "../../../Dataset/Dynamic/Origin/" + name + "/" + name + "_" + to_string(i) + ".adjlist";
            Graph origin_graph(graph_path);
            dynamic_vector.push_back(origin_graph);
            cout << "Reading Completed! : " + name + "_" + to_string(i) << endl;
        }

        graph_map[name] = dynamic_vector;
    }

    for (string name : graph_list) {
        int timestamp = 0;
        for (Graph graph : graph_map[name]) {
            for (string rate : sampling_rate) {
                string size;
                if (rate == "neighbor") {
                    size = size_define(graph);
                } else {
                    size = rate;
                }
                for (string sampling : sampling_list) {
                    vector<int> tmp_list;
                    tmp_list.clear();
                    if (sampling == "TPN") {
                        tmp_list.push_back(0);
                    } else {
                        tmp_list = ver_list;
                    }
                    for (int ver : tmp_list) {
                            Graph sampling_graph = return_sampling_graph(graph, name, size, sampling);
                            if (sampling == "TPN") {
                                for (int j = 0; j < ver_list.size(); j++) {
                                    cout << name << "_" << timestamp << " " << sampling << " RATE=" << rate << " ver=" << j << endl;
                                    string path = "../../../Dataset/Dynamic/Sampling/" + name + "/" + name + "_" + to_string(timestamp) + "/size_" + rate + "/" + sampling + "/ver_" + to_string(j) + "/sampling_graph.adjlist";
                                    write_to_file(path, sampling_graph);
                                }
                            } else {
                                cout << name << "_" << timestamp << " " << sampling << " RATE=" << rate << " ver=" << ver << endl;
                                string path = "../../../Dataset/Dynamic/Sampling/" + name + "/" + name + "_" + to_string(timestamp) + "/size_" + rate + "/" + sampling + "/ver_" + to_string(ver) + "/sampling_graph.adjlist";
                                write_to_file(path, sampling_graph);
                            }
                        }
                    }
                }
            timestamp++;
        }
    }

    return 0;
}
*/