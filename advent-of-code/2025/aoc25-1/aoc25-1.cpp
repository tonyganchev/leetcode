// https://adventofcode.com/2025/day/1

#include <cassert>

import std;

using namespace std;

static constexpr auto dial_ticks = 100;
static constexpr auto dial_buffer = 10 * dial_ticks;

// https://adventofcode.com/2025/day/1#part1
template <typename Stream>
static auto part1(Stream is) {
    is >> skipws;
    auto dial = 50;
    auto counter = 0;
    while (is) {
        char rotation;
        int change;
        is >> rotation >> change;
        if (!is) {
            break;
        }
        assert(rotation == 'R' || rotation == 'L');
        auto op = rotation == 'L' ? -1 : 1;
        dial = (dial + op * change) % dial_ticks;
        if (dial == 0) {
            counter++;
        }
    }
    return counter;
}

static auto count_zeros(int dial, int op, int d) {
    auto old_dial_buffered = dial + dial_buffer;
    auto new_dial_buffered = old_dial_buffered + op * d;
    if (op == -1) {
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
template <typename Stream>
static auto part2(Stream is) {
    is >> skipws;
    auto dial = 50;
    long long counter = 0;
    while (is) {
        char rotation;
        int change;
        is >> rotation >> change;
        if (!is) {
            break;
        }
        assert(rotation == 'R' || rotation == 'L');
        auto op = rotation == 'L' ? -1 : 1;
        auto zeros = count_zeros(dial, op, change);
        counter += zeros;
        dial = (dial + dial_buffer + op * change) % dial_ticks;
    }
    return counter;
}

int main() {
    auto short_vector = R"(L68
L30
R48
L5
R60
L55
L1
L99
R14
L82)"sv;
    // https://adventofcode.com/2025/day/1/input
    static const auto file = "input-vector.txt";

    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream(file)) << endl;

    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream(file)) << endl;

    return 0;
}
