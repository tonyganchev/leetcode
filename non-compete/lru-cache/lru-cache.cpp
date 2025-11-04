#include <cassert>
#include <iostream>
#include <iterator>
#include <list>
#include <unordered_map>

namespace std {
    template<typename F, typename S>
    ostream& operator <<(ostream& os, const pair<F, S>& p) {
        os << p.first << " -> " << p.second;
        return os;
    }
}

using namespace std;

template <typename K, typename V>
class lru_cache {
public:
    using key_type = K;
    using value_type = V;

private:
    using list_type = list<pair<key_type, value_type>>;
    using list_value_type = typename list_type::value_type;
    using map_value_type = typename list_type::iterator;

public:
    lru_cache(const size_t max_size) : max_size_(max_size) { }

    bool contains(const key_type& key) const {
        bump_recency(key);
        return map_.find(key) != map_.end();
    }

    void store(const key_type& key, const value_type& value) {
        list_.push_back(make_pair(key, value));
        auto it = prev(list_.end());
        map_[key] = it;
        while (list_.size() > max_size_) {
            auto entry_to_remove = list_.front();
            map_.erase(entry_to_remove.first);
            list_.pop_front();
        }
    }

    value_type& operator[](const key_type& key) {
        bump_recency(key);
        return *map_[key].second;
    }

    const value_type& operator[](const key_type& key) const {
        bump_recency(key);
        return *map_[key].second;
    }

    size_t size() const {
        return list_.size();
    }

    friend ostream& operator <<(ostream& os, const lru_cache& cache) {
        ostream_iterator<list_value_type> oit { os, "; " };
        copy(cache.list_.cbegin(), cache.list_.cend(), oit);
        return os;
    }

private:
    mutable list_type list_;
    mutable unordered_map<key_type, map_value_type> map_;
    const size_t max_size_;

    void bump_recency(const key_type& key) const {
        auto it = map_.find(key);
        if (it != map_.end()) {
            auto& node_to_bump = it->second;
            list_.splice(list_.end(), list_, it->second);
            map_[key] = prev(list_.end());
        }
    }
};

int main() {
    lru_cache<int, string> cache(5);

    cache.store(1, "one");
    assert(cache.size() == 1);
    cout << cache << endl;

    cache.store(2, "two");
    assert(cache.size() == 2);
    cout << cache << endl;

    cache.store(3, "three");
    assert(cache.size() == 3);
    cout << cache << endl;

    cache.store(4, "four");
    assert(cache.size() == 4);
    cout << cache << endl;

    cache.store(5, "five");
    assert(cache.size() == 5);
    cout << cache << endl;

    cout << "Touching 1" << endl;

    const auto& c = cache;
    c.contains(1);
    cout << cache << endl;

    cache.store(6, "six");
    assert(cache.size() == 5);
    cout << cache << endl;

    cache.store(7, "seven");
    assert(cache.size() == 5);
    cout << cache << endl;

    return 0;
}
