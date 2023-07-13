#include "MyGraph.h"
#include "header.h"

int main()
{
    std::string file_name = "../../Dataset/Origin/Graph/amazon0601.adjlist";

    MyGraph mygraph(file_name);

    std::map<int, int> in_deg_map = mygraph.in_deg_map;

    for (auto itr = in_deg_map.begin(); itr != in_deg_map.end(); itr++) {
        std::cout << "key: " << itr->first << ", value: " << itr->second << std::endl;
    }

    return 0;
}