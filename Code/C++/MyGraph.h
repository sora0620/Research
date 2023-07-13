#ifndef MYGRAPH_H
#define MYGRAPH_H

#include "header.h"
#include "useful.h"

class MyGraph
{
public:
    std::map<int, std::vector <int> > out_neighbor_map; // キーにノード, 値に出隣接ノードのリストの辞書
    std::map<int, std::vector <int> > in_neighbor_map;  // キーにノード, 値に入隣接ノードのリストの辞書
    std::map<int, int> in_deg_map;  // 入次数
    std::map<int, int> out_deg_map; // 出次数
    int number_of_nodes;
    std::vector<int> node_vec; // 全ノードを格納したリスト

    MyGraph(std::string file_name)
    {
        std::ifstream read_file(file_name);

        if (!read_file) {
            std::cerr << "Error!" << std::endl;
            std::exit(1);
        }

        std::vector<std::vector <int> > vec_1;
        std::map<int, std::vector <int> > out_mp;
        std::map<int, std::vector <int> > in_mp;
        std::string string_buf;
        
        while(std::getline(read_file, string_buf)) {
            std::vector<std::string> vec_2;
            std::vector<int> vec_3;
            tokenize(string_buf, ' ', vec_2);
            for (int i = 0; i < vec_2.size(); i++) {
                vec_3.push_back(stoi(vec_2.at(i)));
            }
            vec_1.push_back(vec_3);
        }

        std::vector<int> node_vec;

        for (int i = 0; i < vec_1.size(); i++) {
            for (int j = 0; j < vec_1.at(i).size(); j++) {
                if (std::find(node_vec.begin(), node_vec.end(), vec_1.at(i).at(j)) == node_vec.end()) {
                    node_vec.push_back(vec_1.at(i).at(j));
                }
            }
        }

        this->node_vec = node_vec;
        this->number_of_nodes = node_vec.size();

        for (int i = 0; i < node_vec.size(); i++) {
            in_mp[node_vec.at(i)].empty();
            out_mp[node_vec.at(i)].empty();
        }

        for (int i = 0; i < vec_1.size(); i++) {
            int tmp;
            for (int j = 0; j < vec_1.at(i).size(); j++) {
                if (j == 0) {
                    tmp = vec_1.at(i).at(j);
                } else {
                    in_mp[vec_1.at(i).at(j)].push_back(tmp);
                    out_mp[tmp].push_back(vec_1.at(i).at(j));
                }
            }
        }

        this->out_neighbor_map = out_mp;
        this->in_neighbor_map = in_mp;

        std::map<int, int> out_deg_map;

        for (auto itr = out_mp.begin(); itr != out_mp.end(); itr++) {
            out_deg_map[itr->first] = itr->second.size();
        }

        this->out_deg_map = out_deg_map;

        std::map<int, int> in_deg_map;

        for (auto itr = in_mp.begin(); itr != in_mp.end(); itr++) {
            in_deg_map[itr->first] = itr->second.size();
        }

        this->in_deg_map = in_deg_map;
    }
};

#endif