/*
 * @lc app=leetcode id=146 lang=cpp
 *
 * [146] LRU Cache
 */

// @lc code=start
#include <cassert>
#include <iostream>
#include <unordered_map>
#include <utility>

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
    lru_cache(const size_t max_size) : max_size_(max_size) {}

    bool contains(const key_type& key) const {
        bump_recency(key);
        return map_.find(key) != map_.end();
    }

    void store(const key_type& key, const value_type& value) {
        auto it = map_.find(key);
        if (it == map_.cend()) {
            list_.push_back(make_pair(key, value));
            auto it = prev(list_.end());
            map_[key] = it;
            while (list_.size() > max_size_) {
                map_.erase(list_.front().first);
                list_.pop_front();
            }
        } else {
            bump_recency(key);
            map_[key]->second = value;
        }
    }

    value_type& operator[](const key_type& key) {
        bump_recency(key);
        auto& it = map_[key];
        return it->second;
    }

    const value_type& operator[](const key_type& key) const {
        bump_recency(key);
        auto& it = map_[key];
        return it->second;
    }

    size_t size() const {
        return list_.size();
    }

    friend ostream& operator <<(ostream& os, const lru_cache& cache) {
        ostream_iterator<list_value_type> oit{ os, "; " };
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


class LRUCache {
public:
    LRUCache(int capacity) : cache_(capacity) {}
    
    int get(int key) {
        return cache_[key];
    }
    
    void put(int key, int value) {
        cache_.store(key, value);
    }
private:
    lru_cache<int, int> cache_;
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
// @lc code=end

