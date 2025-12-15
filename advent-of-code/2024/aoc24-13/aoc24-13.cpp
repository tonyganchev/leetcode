#include <cassert>

import std;
import utils;

using namespace std;

// https://adventofcode.com/2024/day/13
template <typename Stream>
static auto solve(Stream& is, intmax_t prize_prefix) {
    intmax_t tokens_spent = 0LL;
    string entry;
    while (getline(is, entry)) {
        intmax_t xa, ya, xb, yb, x, y;
#pragma warning(suppress : 4996)
        sscanf(entry.c_str(), "Button A: X+%lld, Y+%lld", &xa, &ya);
        getline(is, entry);
#pragma warning(suppress : 4996)
        sscanf(entry.c_str(), "Button B: X+%lld, Y+%lld", &xb, &yb);
        getline(is, entry);
#pragma warning(suppress : 4996)
        sscanf(entry.c_str(), "Prize: X=%lld, Y=%lld", &x, &y);
        getline(is, entry);

        x += prize_prefix;
        y += prize_prefix;

        intmax_t da = x * yb - xb * y;
        intmax_t db = xa * y - x * ya;
        intmax_t d = xa * yb - xb * ya;

        if (d == 0) {
            // both A and B buttons have similar "climb angle".

            if (da != 0 || db != 0) {
                assert("no solution" == "!");
            } else {
                assert("infinite solutions" == "!");
            }
        } else {
            if (da % d != 0 || db % d != 0) {
                cout << "no integer solution" << endl;
            } else {
                intmax_t ta = da / d;
                intmax_t tb = db / d;
                if (ta < 0 || tb < 0) {
                    assert("no positive integer solution" == "!");
                } else {
                    intmax_t ts = 3 * ta + tb;
                    cout << ts << endl;
                    tokens_spent += ts;
                }
            }
        }
    }

    return tokens_spent;
}

// https://adventofcode.com/2024/day/13
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts{ "part1" };
    return solve(is, 0LL);
}

// https://adventofcode.com/2024/day/13#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts{ "part2" };
    return solve(is, 10000000000000LL);
}

int main() {
    auto short_vector = R"(Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279)"sv;
//    cout << part1(ispanstream(short_vector)) << endl;
//    cout << part1(ifstream("input-vector.txt")) << endl;
    //cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
