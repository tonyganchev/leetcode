import std;
import utils;

using namespace std;

template <typename Stream>
Stream& operator >>(Stream& is, vector<string>& lines) {
    string line;
    while (getline(is, line)) {
        line += " ";
        lines.push_back(move(line));
    }
    return is;
}

// https://adventofcode.com/2025/day/6
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts;
    vector<string> lines;
    lines.reserve(5);
    is >> lines;
    vector<vector<int>> operands;
    operands.reserve(4);
    auto operand_data = span(lines).first(lines.size() - 1);
    for (const auto& l : operand_data) {
        int n;
        ispanstream is(l);
        operands.emplace_back();
        operands.back().reserve(1100);
        while (is >> n) {
            operands.back().push_back(n);
        }
    }
    ispanstream iss(lines.back());
    char op;
    auto total_results = 0LL;
    for (auto i : views::iota(0uz, operands.front().size())) {
        iss >> op;
        auto result = op == '+' ? 0LL : 1LL;
        for (const auto& l : operands) {
            if (op == '+') {
                result += l[i];
            } else {
                result *= l[i];
            }
        }
        total_results += result;
    }
    return total_results;
}

// https://adventofcode.com/2025/day/6#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts;
    vector<string> lines;
    lines.reserve(5);
    is >> lines;
    auto total_results = 0LL;
    vector<long long> operands;
    operands.reserve(5);
    char current_op = ' ';
    bool digit_found = false;
    long long current_operand = 0LL;
    for (auto j : views::iota(0uz, lines.front().size())) {
        if (lines.back()[j] != ' ') {
            current_op = lines.back()[j];
        }
        for (auto i : views::iota(0uz, lines.size() - 1)) {
            if (lines[i][j] != ' ') {
                current_operand = current_operand * 10 + (lines[i][j] - '0');
                digit_found = true;
            }

            if (i == lines.size() - 2) {
                if (digit_found) {
                    operands.push_back(current_operand);
                    digit_found = false;
                } else {
                    auto result = current_op == '*'
                        ? ranges::fold_left(operands, 1LL, multiplies())
                        : ranges::fold_left(operands, 0LL, plus());
                    total_results += result;
                    operands = {};
                }
                current_operand = 0LL;
            }
        }
    }
    return total_results;
}

int main() {
    auto short_vector = R"(123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  )"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
