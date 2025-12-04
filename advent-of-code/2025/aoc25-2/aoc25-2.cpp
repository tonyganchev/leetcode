#include <cassert>
import std;

using namespace std;

// https://adventofcode.com/2025/day/2
template <typename Stream>
static auto part1(Stream is) {
    auto invalid_id_sum = 0LL;

    char dash;
    long long from, to;
    while (is >> from >> dash >> to) {
        assert(dash == '-');
        // pull the comma out
        is.get();

        long long from_mag = ceil(log10(from));
        if (from_mag % 2 == 1) {
            from = pow(10, from_mag++);
        }
        long long to_mag = ceil(log10(to));
        if (to_mag % 2 == 1) {
            to = pow(10, --to_mag) - 1;
        }
        if (from > to) {
            continue;
        }

        for (auto m = from_mag; m <= to_mag; m += 2) {
            long long hp = pow(10, m / 2);

            for (auto n = from / hp; ; n++) {
                auto v = n * hp + n;
                if (v > to) {
                    break;
                }
                if (v >= from) {
                    invalid_id_sum += v;
                }
            }
        }
    }
    return invalid_id_sum;
}

// https://adventofcode.com/2025/day/2#part2
template <typename Stream>
static auto part2(Stream is) {
    auto invalid_id_sum = 0LL;

    char dash;
    auto checks = 0LL;
    long long from, to;
    while (is >> from >> dash >> to) {
        assert(dash == '-');
        // pull the comma out
        is.get();

        for (auto n : views::iota(from, to + 1)) {
            long long m = ceil(log10(n));
            for (auto k : views::iota(1, m / 2 + 1)) {
                if (m % k != 0) {
                    continue;
                }
                long long p = pow(10, k);
                long long pat = n % p;
                bool match = true;
                auto l = n;
                while (l > 0) {
                    if (l % p != pat) {
                        match = false;
                        break;
                    }
                    l /= p;
                }
                if (match) {
                    invalid_id_sum += n;
                    break;
                }
            }
        }
    }
    return invalid_id_sum;
}

int main() {
    auto short_vector = "\
11-22,\
95-115,\
998-1012,\
1188511880-1188511890,\
222220-222224,\
1698522-1698528,\
446443-446449,\
38593856-38593862,\
565653-565659,\
824824821-824824827,\
2121212118-2121212124"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
