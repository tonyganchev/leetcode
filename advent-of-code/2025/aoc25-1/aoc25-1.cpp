#include <cassert>

import std;
import utils;

using namespace std;

static constexpr auto dial_ticks = 100;
static constexpr auto dial_buffer = 10 * dial_ticks;

// https://adventofcode.com/2025/day/1
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts;

    is >> skipws;
    auto dial = 50;
    auto counter = 0;
    char rotation;
    int change;
    while (is >> rotation >> change) {
        assert(rotation == 'R' || rotation == 'L');
        const auto op = rotation == 'L' ? -1 : 1;
        dial = (dial + op * change) % dial_ticks;
        if (dial == 0) {
            counter++;
        }
    }
    return counter;
}

static auto count_zeros(const int dial, const int op, const int change) {
    auto old_dial_buffered = dial + dial_buffer;
    auto new_dial_buffered = old_dial_buffered + op * change;
    // XXX: I hate myself for writing this corner case hanler...
    if (op == -1) {
        if (dial == 0) {
            old_dial_buffered--;
        }
        if (new_dial_buffered % dial_ticks == 0) {
            new_dial_buffered--;
        }
    }
    const auto zeros = abs(new_dial_buffered / dial_ticks
        - old_dial_buffered / dial_ticks);
    return zeros;
}

// https://adventofcode.com/2025/day/1#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts;

    is >> skipws;
    auto dial = 50;
    auto counter = 0;
    char rotation;
    int change;
    while (is >> rotation >> change) {
        assert(rotation == 'R' || rotation == 'L');
        const auto op = rotation == 'L' ? -1 : 1;
        const auto zeros = count_zeros(dial, op, change);
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
