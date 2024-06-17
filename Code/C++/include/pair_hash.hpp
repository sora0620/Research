#ifndef PAIR_HASH_HPP
#define PAIR_HASH_HPP

template<class T>
size_t HashCombine(const size_t seed,const T &v){
    return seed^(std::hash<T>()(v)+0x9e3779b9+(seed<<6)+(seed>>2));
}
/* pair用 */
struct pairhash{
    template<class T,class S>
    size_t operator()(const std::pair<T,S> &keyval) const noexcept {
        return HashCombine(std::hash<T>()(keyval.first), keyval.second);
    }
};

#endif // PAIR_HASH_HPP