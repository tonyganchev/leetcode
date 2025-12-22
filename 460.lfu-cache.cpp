/*
 * @lc app=leetcode id=460 lang=cpp
 *
 * [460] LFU Cache
 */

 // @lc code=start

#include <cassert>
#include <iostream>
#include <list>
#include <ranges>
#include <unordered_map>

using namespace std;

template<typename K, typename V>
class lfu_cache {

public:

    using key_type = K;
    using value_type = V;

private:

    using freq_t = size_t;

    struct frequency_bucket_item {
        key_type key;
        value_type value;
    };

    struct frequency_bucket {
        size_t freq;
        list<frequency_bucket_item> items;
    };

    struct value_ref {
        list<frequency_bucket>::iterator bucket_it;
        list<frequency_bucket_item>::iterator value_it;
    };

public:

    lfu_cache(size_t capacity) : capacity_(capacity) {
        map_.reserve(capacity);
    }

    auto store(const key_type& k, const value_type& v) {
        if (map_.contains(k)) {
            // overwrite the value for an existing item
            bump_frequency(k);
            map_[k].value_it->value = v;
        } else {
            // no item with the specified key - would add a new item either in
            // place of existing item in a bucket or as a a new item in a
            // bucket.
            if (map_.size() == capacity_) {
                // we are at capacity, We'd pick an item from the lowest-access
                // frequency bucket and either add it to the beginning of the
                // bucket (newest added) or as the sole item in a new bucket of
                // frequency 1.
                auto& forgotten_bucket = freqs_.back();
                map_.erase(forgotten_bucket.items.back().key);
                if (forgotten_bucket.freq == 1uz) {
                    // we should insert the new item at the front of the last
                    // bucket.
                    if (forgotten_bucket.items.size() != 1uz) {
                        // we move the last item at the front to use for the
                        // new value.
                        forgotten_bucket.items.splice(
                            forgotten_bucket.items.begin(),
                            forgotten_bucket.items,
                            prev(forgotten_bucket.items.end()));
                    }
                } else {
                    // the last bucket has higher frequency than one. We should
                    // figure out if we can repurpose it or we need another
                    // bucket.
                    if (forgotten_bucket.items.size() == 1uz) {
                        // repurpose the only node in the last bucket for the
                        // new item and update the frequency.
                        forgotten_bucket.freq = 1;
                    } else {
                        // we create a new bucket and splice the old node from
                        // the old to the new list.
                        freqs_.push_back({});
                        auto& new_bucket = freqs_.back();
                        new_bucket.freq = 1uz;
                        new_bucket.items.splice(
                            new_bucket.items.begin(),
                            forgotten_bucket.items,
                            prev(forgotten_bucket.items.end()));
                    }
                }
                auto& new_item = freqs_.back().items.front();
                new_item.key = k;
                new_item.value = v;
            } else {
                // all existing items are kept alive. We're adding a new item
                // in potentially a new bucket.
                if (freqs_.empty() || freqs_.back().freq != 1uz) {
                    // we put the new item alone in a new bucket.
                    freqs_.push_back({});
                    freqs_.back().freq = 1uz;
                }
                freqs_.back().items.emplace_front(k, v);
            }
            auto bucket_it = prev(freqs_.end());
            auto& mi = map_[k];
            mi.bucket_it = bucket_it;
            auto& last_bucket = freqs_.back();
            mi.value_it = last_bucket.items.begin();
            assert(last_bucket.freq == 1);
            assert(last_bucket.items.front().key == k);
            assert(last_bucket.items.front().value == v);
        }
    }

    auto contains(const key_type& k) {
        return map_.contains(k);
    }

    auto& operator[](const key_type& k) const {
        bump_frequency(k);
        auto& mi = map_[k];
        assert(mi.value_it->key == k);
        return mi.value_it->value;
    }

    auto& operator[](const key_type& k) {
        bump_frequency(k);
        auto& mi = map_[k];
        assert(mi.value_it->key == k);
        return mi.value_it->value;
    }

    friend auto& operator <<(ostream& os, const lfu_cache& cache) {
        for (const auto& [k, v] : cache.map_) {
            os << k << ": " << v.value_it->value << "; ";
        }
        return os;
    }
private:

    auto bump_frequency(const key_type& k) {
        if (!map_.contains(k)) {
            return;
        }
        auto& mi = map_[k];
        auto new_freq = mi.bucket_it->freq + 1;
        decltype(mi.bucket_it) bucket_it;
        if (mi.bucket_it->items.size() == 1uz) {
            assert(mi.bucket_it->items.front().key == k);
            if (mi.bucket_it == freqs_.begin()
                    || prev(mi.bucket_it)->freq != new_freq) {
                mi.bucket_it->freq = new_freq;
                bucket_it = mi.bucket_it;
            } else {
                bucket_it = prev(mi.bucket_it);
                bucket_it->items.splice(
                    bucket_it->items.begin(),
                    mi.bucket_it->items,
                    mi.value_it);
                assert(mi.bucket_it->items.empty());
                freqs_.erase(mi.bucket_it);
            }
        } else {
            if (mi.bucket_it == freqs_.begin()
                || prev(mi.bucket_it)->freq != new_freq) {

                auto it = freqs_.insert(freqs_.begin(), { new_freq, {} });
                assert(it != mi.bucket_it);
            }
            bucket_it = prev(mi.bucket_it);
            bucket_it->freq = new_freq;
            bucket_it->items.splice(
                bucket_it->items.begin(),
                mi.bucket_it->items,
                mi.value_it);
        }
        mi.bucket_it = bucket_it;
    }

    const size_t capacity_;
    mutable unordered_map<key_type, value_ref> map_;
    mutable list<frequency_bucket> freqs_;

};

class LFUCache {
public:
    LFUCache(int capacity) : cache_(capacity) {}

    int get(int key) {
        return cache_.contains(key) ? cache_[key] : -1;
    }

    void put(int key, int value) {
        cache_.store(key, value);
    }
private:
    lfu_cache<int, int> cache_;
};

/**
 * Your LFUCache object will be instantiated and called as such:
 * LFUCache* obj = new LFUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
 // @lc code=end

int main() {
    LFUCache cache(10);

    cache.put(10, 13);
    cache.put(3, 17);
    cache.put(6, 11);
    cache.put(10, 5);
    cache.put(9, 10);
    assert(cache.get(13) == -1);
    cache.put(2, 19);
    assert(cache.get(2) == 19);
    assert(cache.get(3) == 17);
    cache.put(5, 25);
    assert(cache.get(8) == -1);
    cache.put(9, 22);
    cache.put(5, 5);
    cache.put(1, 30);
    assert(cache.get(11) == -1);
    cache.put(9, 12);
    assert(cache.get(7) == -1);
    assert(cache.get(5) == 5);
    assert(cache.get(8) == -1);
    assert(cache.get(9) == 12);
    cache.put(4, 30);
    cache.put(9, 3);
    assert(cache.get(9) == 3);
    assert(cache.get(10) == 5);
    assert(cache.get(10) == 5);
    cache.put(6, 14);
    cache.put(3, 1);
    assert(cache.get(3) == 1);
    cache.put(10, 11);
    assert(cache.get(8) == -1);
    cache.put(2, 14);
    assert(cache.get(1) == 30);
    assert(cache.get(5) == 5);
    assert(cache.get(4) == 30);
    cache.put(11, 4);
    cache.put(12, 24);
    cache.put(5, 18);
    assert(cache.get(13) == -1);
    cache.put(7, 23);
    assert(cache.get(8) == -1);
    assert(cache.get(12) == 24);
    cache.put(3, 27);
    cache.put(2, 12);
    assert(cache.get(5) == 18);
    cache.put(2, 9);
    cache.put(13, 4);
    cache.put(8, 18);
    cache.put(1, 7);
    assert(cache.get(6) == 14);
    cache.put(9, 29);
    cache.put(8, 21);
    assert(cache.get(5) == 18);
    cache.put(6, 30);
    cache.put(1, 12);
    assert(cache.get(10) == 11);
    cache.put(4, 15);
    cache.put(7, 22);
    cache.put(11, 26);
    cache.put(8, 17);
    cache.put(9, 29);
    assert(cache.get(5) == 18);
    cache.put(3, 4);
    cache.put(11, 30);
    assert(cache.get(12) == -1);
    cache.put(4, 29);
    assert(cache.get(3) == 4);
    assert(cache.get(9) == 29);
    assert(cache.get(6) == 30);
    cache.put(3, 4);
    assert(cache.get(1) == 12);
    assert(cache.get(10) == 11);
    cache.put(3, 29);
    cache.put(10, 28);
    cache.put(1, 20);
    cache.put(11, 13);
    assert(cache.get(3) == 29);
    cache.put(3, 12);
    cache.put(3, 8);
    cache.put(10, 9);
    cache.put(3, 26);
    assert(cache.get(8) == 17);
    assert(cache.get(7) == -1);
    assert(cache.get(5) == 18);
    cache.put(13, 17);
    cache.put(2, 27);
    cache.put(11, 15);
    assert(cache.get(12) == -1);
    cache.put(9, 19);
    cache.put(2, 15);
    cache.put(3, 16);
    assert(cache.get(1) == 20);
    cache.put(12, 17);
    cache.put(9, 1);
    cache.put(6, 19);
    assert(cache.get(4) == 29);
    assert(cache.get(5) == 18);
    assert(cache.get(5) == 18);
    cache.put(8, 1);
    cache.put(11, 7);
    cache.put(5, 2);
    cache.put(9, 28);
    assert(cache.get(1) == 20);
    cache.put(2, 2);
    cache.put(7, 4);
    cache.put(4, 22);
    cache.put(7, 24);
    cache.put(9, 26);
    cache.put(13, 28);
    cache.put(11, 26);

    return 0;
}
