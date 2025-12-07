import std;
import utils;

using namespace std;

namespace std {
    template <>
    struct hash<pair<int, int>> {
        std::size_t operator ()(const pair<int, int>& pt) const {
            return pt.first << 16 ^ pt.second;
        }
    };

    ostream& operator << (ostream& os, const pair<int, int>& p) {
        os << p.first << ":" << p.second;
        return os;
    }
}

template <typename Stream>
Stream& operator >>(Stream& is, vector<string>& lines) {
    string line;
    while (getline(is, line)) {
        lines.push_back(move(line));
    }
    return is;
}

// https://adventofcode.com/2024/day/10
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts{ "part1" };
    vector<string> map;
    is >> map;
    //ranges::copy(map, ostream_iterator<string>(cout, "\n"));
    vector<vector<unordered_set<pair<int, int>>>> reachable_paths(
        map.size(),
        vector<unordered_set<pair<int, int>>>(map.front().size(), {})
    );

    auto score = 0LL;
    for (auto i : views::iota(0uz, map.size())) {
        for (auto j : views::iota(0uz, map.front().size())) {
            if (map[i][j] != '9') {
                continue;
            }
            deque<pair<int, int>> paths = { { i, j } };
            while (!paths.empty()) {
                const auto [pi, pj] = paths.front();
                paths.pop_front();
                if (reachable_paths[pi][pj].contains({ i, j })) {
                    continue;
                }
                reachable_paths[pi][pj].insert({ i, j });
                for (auto di : views::iota(-1, 2)) {
                    for (auto dj : views::iota(-1, 2)) {
                        if (abs(di - dj) != 1) {
                            continue;
                        }
                        auto ni = pi + di;
                        auto nj = pj + dj;
                        if (ni >= 0 && ni < map.size()
                            && nj >= 0 && nj < map.front().size()
                            && map[ni][nj] - map[pi][pj] == -1) {
                            paths.emplace_back(ni, nj);
                        }
                    }
                }
            }
        }
    }
    for (auto i : views::iota(0uz, map.size())) {
        for (auto j : views::iota(0uz, map.front().size())) {
            if (map[i][j] == '0') {
                score += reachable_paths[i][j].size();
            }
        }
    }
    return score;
}

static auto rankings_from(
    const vector<string>& map,
    const int i,
    const int j,
    vector<vector<long long>>& cache) {
    auto& v = cache[i][j];
    if (v != -1LL) {
        return v;
    }
    v = 0;
    if (map[i][j] == '9') {
        v = 1;
    } else {
        for (auto di : views::iota(-1, 2)) {
            for (auto dj : views::iota(-1, 2)) {
                if (abs(di - dj) != 1) {
                    continue;
                }
                auto ni = i + di;
                auto nj = j + dj;
                if (ni >= 0 && ni < map.size()
                    && nj >= 0 && nj < map.front().size()
                    && map[ni][nj] - map[i][j] == 1) {
                    v += rankings_from(map, ni, nj, cache);
                }
            }
        }
    }
    return v;
}

// https://adventofcode.com/2024/day/10#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts{ "part2" };
    vector<string> map;
    is >> map;
    vector<vector<long long>> cache(
        map.size(),
        vector<long long>(map.front().size(), -1LL)
    );
    auto rankings = 0LL;
    for (auto i : views::iota(0uz, map.size())) {
        for (auto j : views::iota(0uz, map.front().size())) {
            if (map[i][j] == '0') {
                rankings += rankings_from(map, i, j, cache);
            }
        }
    }
    return rankings;
}

int main() {
    auto short_vector = R"(89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
