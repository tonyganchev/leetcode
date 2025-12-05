import std;

using namespace std;

template <typename Stream>
auto& operator >>(Stream& is, vector<string>& grid) {
    grid.clear();
    grid.reserve(150);
    grid.push_back("");
    grid.push_back(".");
    
    char c;
    is >> noskipws;
    while (is >> c) {
        if (c == '\n') {
            grid.back() += '.';
            if (grid.size() == 2) {
                grid.front() = string(grid.back().length(), '.');
            }
            string new_line;
            if (grid.size() > 2) {
                new_line.reserve(grid.front().length() + 1);
            }
            new_line = ".";
            grid.emplace_back(move(new_line));
        } else {
            grid.back() += c;
        }
    }
    grid.back() += '.';
    grid.push_back(string(grid.back().length(), '.'));

    return is;
}

static auto remove_free(vector<string>& grid) {
    auto free_count = 0;
    
    vector<pair<size_t, size_t>> to_remove;
    to_remove.reserve(2000);
    for (auto i : views::iota(1u, grid.size() - 1)) {
        for (auto j : views::iota(1u, grid.front().size() - 1)) {
            if (grid[i][j] != '@') {
                continue;
            }
            auto n = 0;
            for (auto di : views::iota(-1, 2)) {
                for (auto dj : views::iota(-1, 2)) {
                    if (grid[i + di][j + dj] == '@') {
                        n++;
                    }
                }
            }
            if (n <= 4) {
                to_remove.push_back(make_pair(i, j));
                free_count++;
            }
        }
    }
    for (const auto [i, j] : to_remove) {
        grid[i][j] = '.';
    }

    ranges::copy(grid, ostream_iterator<string>(cout, "\n"));
    cout << endl;

    return free_count;
}

// https://adventofcode.com/2025/day/4
template <typename Stream>
static auto part1(Stream is) {
    vector<string> grid;
    is >> grid;

    return remove_free(grid);
}

// https://adventofcode.com/2025/day/4#part2
template <typename Stream>
static auto part2(Stream is) {
    vector<string> grid;
    is >> grid;

    auto free_count = 0;
    int f;
    while ((f = remove_free(grid)) > 0) {
        free_count += f;
    }
    return free_count;
}

int main() {
    auto short_vector = R"(..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
