#include <cassert>

import std;

using namespace std;

using bound_t = intmax_t;
using range_t = pair<bound_t, bound_t>;

class range_pool {
public:
    using container_type = map<bound_t, bound_t>;
    using iterator = container_type::iterator;
    using const_iterator = container_type::const_iterator;

    auto add(bound_t from, bound_t to) {
        assert(from <= to);
        // add the new range or modify an existing one already starting from
        // `from`.
        auto [it, success] = ranges_.insert({ from, to });
        if (!success) {
            it->second = max(it->second, to);
        }
        // normalize the ranges so that there are no overlaps.

        // Go to the previous range in case the newly-added one merges into it.
        if (it != ranges_.begin()) {
            it = prev(it);
        }
        for (; it != ranges_.end(); ++it) {
            // collapse all subsequent ranges that overlap with the one pointed
            // by `it`.
            auto nit = next(it);
            while (nit != ranges_.end() && it->second >= nit->first) {
                it->second = max(it->second, nit->second);
                ranges_.erase(nit);
                nit = next(it);
            }
        }
    }

    auto begin() {
        return ranges_.begin();
    }
    
    auto cbegin() const {
        return ranges_.cbegin();
    }

    auto end() {
        return ranges_.end();
    }
    
    auto cend() const {
        return ranges_.cend();
    }

    auto find(bound_t needle) const {
        return const_cast<range_pool*>(this)->find_(needle);
    }

private:
    container_type ranges_;

    iterator find_(bound_t needle) {
        for (auto it = ranges_.begin(); it != ranges_.cend(); ++it) {
            if (it->first <= needle && needle <= it->second) {
                return it;
            }
        }
        return ranges_.end();
    }
};

template <typename Stream>
static Stream& operator >>(Stream& is, range_pool& rp) {
    is >> noskipws;
    bound_t from;
    while (is >> from) {
        bound_t to;
        assert(is.get() == '-');
        is >> to;
        assert(is.get() == '\n');
        rp.add(from, to);
    }
    return is;
}


// https://adventofcode.com/2025/day/5
template <typename Stream>
static auto part1(Stream is) {
    range_pool rp;
    is >> rp;
    is.clear();
    is >> skipws;
    bound_t id;
    auto invalid_count = 0LL;
    while (is >> id) {
        auto r = rp.find(id);
        if (r != rp.cend()) {
            invalid_count++;
        }
    }
    return invalid_count;
}

// https://adventofcode.com/2025/day/5#part2
template <typename Stream>
static auto part2(Stream is) {
    range_pool rp;
    is >> rp;
    static_assert(ranges::range<range_pool>);
    return ranges::fold_left(rp, 0, [](long long cur_sum, const auto& p) {
        auto& [from, to] = p;
        return cur_sum + to - from + 1;
    });
}

int main() {
    auto short_vector = R"(3-5
10-14
16-20
12-18

1
5
8
11
17
32)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
