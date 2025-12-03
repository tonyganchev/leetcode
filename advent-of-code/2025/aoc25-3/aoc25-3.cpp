import std;

using namespace std;

template <typename Stream>
static auto solve(Stream& is, const int count) {
    auto sum_joltage = 0LL;
    string bank;
    while (is >> bank) {

        auto sj = 0LL;
        auto it = bank.cbegin();
        for (auto i = count; i > 0; i--) {
            auto rng = ranges::subrange(it, prev(bank.cend(), i - 1));
            it = ranges::max_element(rng);
            sj = 10 * sj + *it - '0';
            it++;
        }
        sum_joltage += sj;
    }
    return sum_joltage;
}

// https://adventofcode.com/2025/day/3
template <typename Stream>
static auto part1(Stream is) {
    return solve(is, 2);
}

// https://adventofcode.com/2025/day/3#part2
template <typename Stream>
static auto part2(Stream is) {
    return solve(is, 12);
}

int main() {
    auto short_vector = R"(987654321111111
811111111111119
234234234234278
818181911112111)"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    /*
    */
    return 0;
}
////