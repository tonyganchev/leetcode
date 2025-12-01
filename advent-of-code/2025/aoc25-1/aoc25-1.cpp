// https://adventofcode.com/2025/day/1

#include <cassert>

import std;

using namespace std;

static constexpr auto dial_ticks = 100;
static constexpr auto dial_buffer = 10 * dial_ticks;

// https://adventofcode.com/2025/day/1#part1
static auto part1(istream& is) {
    is >> skipws;
    auto dial = 50;
    auto counter = 0;
    while (is) {
        char c;
        int d;
        is >> c >> d;
        assert(c == 'R' || c == 'L');
        auto op = c == 'L' ? -1 : 1;
        dial = (dial + op * d) % dial_ticks;
        if (dial == 0) {
            counter++;
        }
    }
    return counter;
}

static auto count_zeros(int dial, int op, int d) {
    auto old_dial_buffered = dial + dial_buffer;
    auto new_dial_buffered = old_dial_buffered + op * d;
    if (op == -1)
    {
        if (dial == 0) {
            old_dial_buffered--;
        }
        if (new_dial_buffered % dial_ticks == 0) {
            new_dial_buffered--;
        }
    }
    auto zeros = abs(new_dial_buffered / dial_ticks
        - old_dial_buffered / dial_ticks);
    return zeros;
}

// https://adventofcode.com/2025/day/1#part2
static auto part2(istream& is) {
    is >> skipws;
    auto dial = 50;
    long long counter = 0;
    while (!is.eof() && !is.bad() && !is.fail()) {
        char c;
        int d;
        is >> c >> d;
        assert(c == 'R' || c == 'L');
        auto op = c == 'L' ? -1 : 1;
        auto zeros = count_zeros(dial, op, d);
        counter += zeros;
        dial = (dial + dial_buffer + op * d) % dial_ticks;
    }
    return counter;
}

int main() {
    auto short_vector = ispanstream{ R"(L68
L30
R48
L5
R60
L55
L1
L99
R14
L82)"sv };
    // https://adventofcode.com/2025/day/1/input
    ifstream long_vector{ "input-vector.txt" };

    cout << part1(short_vector) << endl;
    cout << part1(long_vector) << endl;

    short_vector.clear();
    short_vector.seekg(0);

    long_vector.clear();
    long_vector.seekg(0);

    cout << part2(short_vector) << endl;
    cout << part2(long_vector) << endl;

    return 0;
}
