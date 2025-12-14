#include <cassert>

import std;
import utils;

using namespace std;

static const char border_plot = '_';
template <typename Stream>
Stream& operator >>(Stream& is, vector<string>& grid) {
    grid.clear();
    grid.reserve(145);
    string line;
    while (is >> line) {
        auto line_length = line.length();
        if (grid.empty()) {
            grid.emplace_back(line_length + 2, border_plot);
        }
        grid.emplace_back();
        grid.back() += border_plot;
        grid.back() += line;
        grid.back() += border_plot;
    }
    grid.emplace_back(grid.front().length(), border_plot);
    return is;
}

// https://adventofcode.com/2024/day/12
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts{ "part1" };
    vector<string> grid;
    is >> grid;

    auto result = 0uz;
    for (auto i0 : views::iota(1uz, grid.size() - 1)) {
        for (auto j0 : views::iota(1uz, grid[i0].size() - 1)) {
            char plot = grid[i0][j0];
            if (plot <= 'Z') {
                auto area = 0uz;
                auto circumference = 0uz;
                deque<pair<size_t, size_t>> q = { { i0, j0 } };
                while (!q.empty()) {
                    auto [i, j] = q.front();
                    q.pop_front();
                    if (grid[i][j] != plot) {
                        continue;
                    }
                    area++;
                    grid[i][j] += 'a' - 'A';

                    for (auto di : views::iota(-1, 2)) {
                        for (auto dj : views::iota(-1, 2)) {
                            if (di * di == dj * dj) {
                                continue;
                            }
                            auto ni = i + di;
                            auto nj = j + dj;
                            if (grid[ni][nj] == plot) {

                                q.emplace_back(ni, nj);
                            } else if (grid[ni][nj] != plot + 'a' - 'A') {
                                circumference++;
                            }
                        }
                    }
                }
                result += area * circumference;
            }
        }
    }

    return result;
}


// https://adventofcode.com/2024/day/12#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts{ "part2" };
    vector<string> grid;
    is >> grid;

    auto result = 0uz;
    for (auto i0 : views::iota(1uz, grid.size() - 1)) {
        for (auto j0 : views::iota(1uz, grid[i0].size() - 1)) {
            char plot = grid[i0][j0];
            char visited_plot = grid[i0][j0] + ('a' - 'A');
            if (plot <= 'Z') {
                auto area = 0uz;
                unordered_map<size_t, set<size_t>> hborders;
                unordered_map<size_t, set<size_t>> vborders;
                deque<pair<size_t, size_t>> q = { { i0, j0 } };
                while (!q.empty()) {
                    auto [i, j] = q.front();
                    q.pop_front();
                    if (grid[i][j] != plot) {
                        continue;
                    }
                    area++;
                    grid[i][j] = visited_plot;

                    for (auto di : views::iota(-1, 2)) {
                        for (auto dj : views::iota(-1, 2)) {
                            if (di * di == dj * dj) {
                                continue;
                            }
                            auto ni = i + di;
                            auto nj = j + dj;
                            if (grid[ni][nj] == plot) {

                                q.emplace_back(ni, nj);
                            } else if (grid[ni][nj] != visited_plot) {
                                if (di == 0) {
                                    vborders[j + (dj + 1) / 2].insert(i);
                                } else {
                                    hborders[i + (di + 1) / 2].insert(j);
                                }
                            }
                        }
                    }
                }

                auto sides = 0uz;
                for (const auto& [j, vb] : vborders) {
                    auto prev_i = -1;
                    for (auto i : vb) {
                        assert(grid[i][j - 1] == visited_plot
                            || grid[i][j] == visited_plot);
                        if (i - prev_i > 1
                            || (grid[i][j - 1] == visited_plot
                                && grid[prev_i][j - 1] != visited_plot)
                            || (grid[i][j] == visited_plot
                                && grid[prev_i][j] != visited_plot)) {
                            sides++;
                        }
                        prev_i = i;
                    }
                }
                for (const auto& [i, hb] : hborders) {
                    auto prev_j = -1;
                    for (auto j : hb) {
                        assert(grid[i - 1][j] == visited_plot
                            || grid[i][j] == visited_plot);
                        if (j - prev_j > 1
                            || (grid[i - 1][j] == visited_plot
                                && grid[i - 1][prev_j] != visited_plot)
                            || (grid[i][j] == visited_plot
                                && grid[i][prev_j] != visited_plot)) {
                            sides++;
                        }
                        prev_j = j;
                    }
                }
                result += area * sides;
            }
        }
    }

    return result;
}

int main() {
    auto short_vector = R"(RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
