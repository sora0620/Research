#ifndef GUARD_WRITE
#define GUARD_WRITE

#include <unordered_map>
#include <fstream>
#include "./json.hpp"

using json = nlohmann::json;

void write_json(string path, unordered_map<int, double> m)
{
    ofstream ofs(path);
    if (ofs.good())
    {
        json m_json;

        for (auto [node, value] : m) {
            m_json[to_string(node)] = value;
        }

        ofs << m_json.dump(4);
    }
    else
    {
        cout << "ファイルの読み込みに失敗しました" << endl;
    }
}

#endif