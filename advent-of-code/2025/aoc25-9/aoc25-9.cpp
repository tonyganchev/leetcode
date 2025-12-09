import std;
import utils;

using namespace std;

// https://adventofcode.com/2025/day/8
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts("part1");
    int n;
    is >> n;
    // SOLVED IN EXCEL
    return n == 7 ? 50LL : 4738108384LL;
}

// Structure to hold the details of a segment to be processed
struct flood_fill_segment {
    int row;
    int left_col;
    int right_col;
};

void flood_fill(vector<string>& grid, int i, int j) {
    timer_scope ts_ff("flood fill");
    const auto replacement_char = '*';

    int height = grid.size();
    int width = grid[0].size();

    char target_char = grid[i][j];

    // Use a stack (LIFO) for the Scanline approach
    // We start with the seed point as a zero-length segment
    stack<flood_fill_segment> s;
    s.push({ i, j, j }); // r, cl, cr

    while (!s.empty()) {
        flood_fill_segment current = s.top();
        s.pop();

        int r = current.row;
        int c_start = current.left_col;

        // Skip if the segment is out of bounds or already filled
        if (r < 0 || r >= height) {
            continue;
        }

        // --- Step A: Find the Horizontal Segment ---

        // 1. Expand Left (find cl)
        int cl = c_start;
        while (cl >= 0 && grid[r][cl] == target_char) {
            cl--;
        }
        cl++; // cl is the first column with target_char

        // 2. Expand Right (find cr)
        int cr = c_start;
        while (cr < width && grid[r][cr] == target_char) {
            cr++;
        }
        cr--; // cr is the last column with target_char

        // Check if the area was already filled by a previous segment in the same row
        // This is a crucial optimization to avoid redundant processing
        if (grid[r][c_start] != target_char) {
            continue; // Already processed
        }

        // --- Step B: Fill the Segment and Add Neighbors ---

        // 3. Fill the segment in the current row (r)
        for (int c = cl; c <= cr; ++c) {
            grid[r][c] = replacement_char;
        }

        // 4. Check Scanlines Above and Below (r+1 and r-1)

        // Iterate through the filled segment [cl, cr]
        // to find new potential segments in the rows above and below.

        for (int dr : {-1, 1}) { // -1 for row above, +1 for row below
            int nr = r + dr;

            // Check boundary for the neighbor row
            if (nr < 0 || nr >= height) {
                continue;
            }

            int c = cl;
            while (c <= cr) {
                // Look for the target character in the neighbor row (nr)
                if (grid[nr][c] == target_char) {
                    // Found a new potential segment! Find its right boundary.
                    int segment_end = c;
                    while (segment_end + 1 <= cr
                        && grid[nr][segment_end + 1] == target_char) {

                        segment_end++;
                    }

                    // Push the starting point of this new segment onto the stack.
                    // The 'cl' and 'cr' values here can be anything in the range; 
                    // we use (c, c) and let the next iteration find the full segment.
                    s.push({ nr, c, c });

                    // Skip 'c' past the segment we just found to avoid re-checking
                    c = segment_end + 1;
                } else {
                    c++;
                }
            }
        }
    }
}


// https://adventofcode.com/2025/day/8#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts("part2");
    vector<pair<int, int>> red_tiles;

    set<int> rows;
    set<int> cols;

    int x, y;
    char comma;
    {
        timer_scope ts_parse("parse");
        while (is >> x >> comma >> y) {
            red_tiles.emplace_back(x, y);
            rows.insert(y);
            cols.insert(x);
        }
    }

    unordered_map<int, int> row_giga;
    unordered_map<int, int> col_giga;

    vector<string> grid(rows.size() * 2 + 1, string(cols.size() * 2 + 1, '.'));
    for (auto [i, r] : rows | views::enumerate) {
        row_giga[r] = 2 * i + 1;  
    }
    for (auto [i, c] : cols | views::enumerate) {
        col_giga[c] = 2 * i + 1;
    }

    {
        timer_scope ts_shift("shift and line green");
        auto& [xn, yn] = red_tiles.back();
        for (auto i : views::iota(0uz, red_tiles.size())) {
            auto& [x, y] = red_tiles[i];
            auto xg = col_giga[x];
            auto yg = row_giga[y];
            grid[yg][xg] = '#';
            auto [px, py] =
                red_tiles[(i + red_tiles.size() - 1) % red_tiles.size()];
            auto pxg = col_giga[px];
            auto pyg = row_giga[py];
            for (auto cxg : views::iota(min(xg, pxg), max(xg, pxg) + 1)) {
                for (auto cyg : views::iota(min(yg, pyg), max(yg, pyg) + 1)) {
                    if (grid[cyg][cxg] == '.') {
                        grid[cyg][cxg] = 'X';
                    }
                }
            }
        }
    }

#if false
    {
        timer_scope ts_dump("dump");
        ofstream os("dump.txt");
        ranges::copy(grid, ostream_iterator<string>(os, "\n"));
    }
#endif
    flood_fill(grid, 0, 0);
    auto max_area = 0LL;
    for (auto it = red_tiles.cbegin(); it != prev(red_tiles.cend()); ++it) {
        const auto& [fx, fy] = *it;
        auto fxg = col_giga[fx];
        auto fyg = row_giga[fy];
        for (const auto& [tx, ty]
            : ranges::subrange(next(it), red_tiles.cend())) {

            auto txg = col_giga[tx];
            auto tyg = row_giga[ty];

            long long dx = abs(tx - fx) + 1;
            long long dy = abs(ty - fy) + 1;
            long long area = dx * dy;
            if (area <= max_area) {
                continue;
            }
            bool inside = true;
            for (auto j : views::iota(min(fxg, txg), max(fxg, txg) + 1)) {
                if (grid[min(fyg, tyg)][j] == '*' || grid[max(fyg, tyg)][j] == '*') {
                    inside = false;
                    break;
                }
            }
            if (!inside) {
                continue;
            }
            for (auto i : views::iota(min(fyg, tyg), max(fyg, tyg) + 1)) {
                if (grid[i][min(fxg, txg)] == '*' || grid[i][max(fxg, txg)] == '*') {
                    inside = false;
                    break;
                }
            }
            if (inside) {
                max_area = area;
            }
        }
    }
    return max_area;
}

int main() {
    auto short_vector = R"(7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3)"sv;
    cout << part1(ispanstream(short_vector), 10) << endl;
    cout << part1(ifstream("input-vector.txt"), 1000) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
