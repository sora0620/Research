#include "header.h"

void print(int x)
{
    std::cout << x << std::endl;
}

void print(double x)
{
    std::cout << x << std::endl;
}

void print(std::map<int, int> m)
{
    for (auto itr = m.begin(); itr != m.end(); itr++) {
        std::cout << "key: " << itr->first << ", value: " << itr->second << std::endl;
    }

    return;
}

void print(std::map<int, double> m)
{
    for (auto itr = m.begin(); itr != m.end(); itr++) {
        std::cout << "key: " << itr->first << ", value: " << itr->second << std::endl;
    }

    return;
}

void print(std::map<int, std::vector <int> > m)
{
    for (auto itr = m.begin(); itr != m.end(); itr++) {
        std::cout << "key: " << itr->first << ", values: ";

        for (int i = 0; i < itr->second.size(); i++) {
            std::cout << itr->second.at(i);

            if (i != itr->second.size() - 1) {
                std::cout << ", ";
            }
        }

        std::cout << std::endl;
    }

    return;
}

void print(std::vector<int> v)
{
    std::cout << "[";

    for (int i = 0; i < v.size(); i++) {
        std::cout << v.at(i);

        if (i != v.size() - 1) {
            std::cout << ", ";
        }
    }

    std::cout << "]" << std::endl;

    return;
}

void tokenize(std::string const &str, const char delim, std::vector<std::string> &out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}
