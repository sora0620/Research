#pragma once

#ifndef GUARD_UTIL_H
#define GUARD_UTIL_H

#include <sys/time.h>
#include <sys/resource.h>
#include <assert.h>

#include <random>
#include <chrono>
#include <vector>
#include <utility>


class RandNumGenerator
{
public:
    virtual int gen(int upper_bound) = 0;
    virtual float gen_float(float upper_bound) = 0;
    virtual ~RandNumGenerator() {}
};

class StdRandNumGenerator : public RandNumGenerator
{
    std::random_device *rd;
    std::mt19937 *mt;
public:
    StdRandNumGenerator()
    {
        rd = new std::random_device();
        mt = new std::mt19937((*rd)());
    }
    ~StdRandNumGenerator()
    {
        delete mt;
        delete rd;
    }
    int gen(int upper_bound)
    {
        std::uniform_int_distribution<int> dis(0, upper_bound - 1);
        return dis(*mt);
    }
    int genRandHostId(int mi, int ma) 
    {
        std::uniform_int_distribution<int> dis(mi, ma);
        return dis(*mt);
    }
    float gen_float(float upper_bound)
    {
        std::uniform_real_distribution<float> dis(0.0, upper_bound);
        return dis(*mt);
    }
    void gen_sample(vector<int> origin_vec, vector<int>& return_vec, int get_num)
    {
        std::sample(origin_vec.begin(), origin_vec.end(), std::back_inserter(return_vec), get_num, *mt);
    }
    void gen_sample_pair(vector<pair <int, int> > origin_vec, vector<pair <int, int> >& return_vec, int get_num)
    {
        std::sample(origin_vec.begin(), origin_vec.end(), std::back_inserter(return_vec), get_num, *mt);
    }
};

//Timer is used for performance profiling
class Timer
{
    std::chrono::time_point<std::chrono::system_clock> _start = std::chrono::system_clock::now();
public:
    void restart()
    {
        _start = std::chrono::system_clock::now();
    }
    double duration()
    {
        std::chrono::duration<double> diff = std::chrono::system_clock::now() - _start;
        return diff.count();
    }
    static double current_time()
    {
        std::chrono::duration<double> val = std::chrono::system_clock::now().time_since_epoch();
        return val.count();
    }
};

#endif // GUARD_UTIL_H