#include <cassert>
import std;

using namespace std;

static auto mag(long long n) {
    auto m = 0LL;
    while (n > 0) {
        m++;
        n /= 10;
    }
    return m;
}

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

        for (auto n : views::iota(from, to + 1)) {
            auto m = mag(n);
            if (m % 2 == 0) {
                long long power = pow(10, m / 2);
                if (n / power == n % power) {
                    invalid_id_sum += n;
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
    long long from, to;
    while (is >> from >> dash >> to) {
        assert(dash == '-');
        // pull the comma out
        is.get();

        for (auto n : views::iota(from, to + 1)) {
            auto m = mag(n);
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
