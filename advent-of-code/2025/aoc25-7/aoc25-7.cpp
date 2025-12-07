import std;
import utils;

using namespace std;

template <typename Stream>
Stream& operator >>(Stream& is, vector<string>& lines) {
    string line;
    while (getline(is, line)) {
        lines.push_back(move(line));
    }
    return is;
}

ostream& operator <<(ostream& os, const vector<string>& lines) {
    ranges::copy(lines, ostream_iterator<string>(os, "\n"));
    return os;
}


// https://adventofcode.com/2024/day/10
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts{ "part1" };
    vector<string> map;
    map.reserve(142);
    is >> map;
    map[0][map.front().size() / 2] = '.';
    auto splits = 0LL;
    deque < pair<int, int>> beams = { { 0, map.front().size() / 2 } };
    while (!beams.empty()) {
        const auto [i, j] = beams.front();
        beams.pop_front();
        if (i >= map.size() || j < 0 || j >= map.front().size()) {
            continue;
        }
        if (map[i][j] == '.') {
            beams.emplace_back(i + 1, j);
            map[i][j] = '|';
        } else if (map[i][j] == '^') {
            splits += 1;
            beams.emplace_back(i, j - 1);
            beams.emplace_back(i, j + 1);
        }
    }
    return splits;
}

static auto paths_from(
    const vector<string>& map,
    const int i,
    const int j,
    vector<vector<long long>>& cache) {

    if (i >= map.size()) {
        return 1LL;
    }
    if (j < 0 || j > map.front().size()) {
        return 0LL;
    }
    auto& v = cache[i][j];
    if (v != -1LL) {
        return v;
    }
    if (map[i][j] == '.') {
        v = paths_from(map, i + 1, j, cache);
    } else if (map[i][j] == '^') {
        v = paths_from(map, i, j - 1, cache)
            + paths_from(map, i, j + 1, cache);
    } else {
        throw domain_error("unexpected map character");
    }
    return v;
}

// https://adventofcode.com/2024/day/10#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts{ "part2" };
    vector<string> map;
    map.reserve(142);
    is >> map;

    auto sj = map.front().size() / 2;
    map[0][sj] = '.';
    vector<vector<long long>> cache(
        map.size(),
        vector<long long>(map.front().size(), -1LL));
    return paths_from(map, 0, sj, cache);
}

int main() {
    auto short_vector = R"(.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
