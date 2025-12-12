#include <cassert>

import std;
import utils;

using namespace std;

using lamps_t = unsigned;
using lamp_mask_t = unsigned;

namespace std {
    template<>
    struct hash<vector<int>> {
        size_t operator ()(const vector<int>& v) const noexcept {
            auto r = v.size();
            for (auto n : v) {
                r ^= n + 0x9e3779b9 + (r << 6) + (r >> 2);
            }
            return r;
        }
    };
}

static inline auto encode_lamps(const string& decoded_lamps) {
    lamps_t encoded_lamps = 0u;
    for (auto c : decoded_lamps | views::reverse) {
        encoded_lamps = (encoded_lamps << 1) | (c == '#' ? 1 : 0);
    }
    return encoded_lamps;
}

static inline auto encode_button_effects_for_lamps(
    const vector<int>& decoded_button_effects) {

    lamp_mask_t encoded_button_effects = 0u;
    for (auto be : decoded_button_effects) {
        encoded_button_effects |= (1 << be);
    }
    return encoded_button_effects;
}

static inline auto decode_lamps(lamps_t encoded_lamps) {
    string s = "";
    while (encoded_lamps != 0) {
        s += (encoded_lamps & 1) == 1 ? '#' : '.';
    }
    ranges::reverse(s);
    return s;
}

lamps_t press_button_for_lamps(
    const lamps_t lamps,
    const lamp_mask_t button_effects) {

    return lamps ^ button_effects;
}

static auto find_minimum_presses_for_lamps(
    const lamps_t current_lamps,
    const lamps_t desired_lamps,
    unordered_set<lamps_t>& passed_lamps,
    const vector<lamp_mask_t>& button_effects,
    size_t best_so_far) {

    if (passed_lamps.size() >= best_so_far) {
        return best_so_far;
    }

    if (current_lamps == desired_lamps) {
        return passed_lamps.size();
    }

    auto min_presses = numeric_limits<long long>::max();
    for (const auto& be : button_effects) {
        lamps_t new_lamps = press_button_for_lamps(current_lamps, be);
        if (!passed_lamps.contains(new_lamps)) {
            passed_lamps.insert(new_lamps);
            auto r = find_minimum_presses_for_lamps(
                new_lamps,
                desired_lamps,
                passed_lamps,
                button_effects,
                best_so_far);
            best_so_far = min(best_so_far, r);
            passed_lamps.erase(new_lamps);
        }
    }

    return best_so_far;
}

// https://adventofcode.com/2025/day/10
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts("part1");
    char c;
    auto result = 0LL;
    while (true) {
        is >> c;
        if (!is) {
            return result;
        }
        assert(c == '[');
        string lamps;
        getline(is, lamps, ']');
        vector<lamp_mask_t> button_effects;
        unordered_set<lamps_t> passed_lamps;
        while (true) {
            is >> c;
            if (c == '{') {
                assert(passed_lamps.size() == 0);
                cout << "--------------------------------------------------\n";
                timer_scope ts_run(lamps.c_str());

                auto desired_lamps = encode_lamps(lamps);
                auto collateral_lamps = 0u;

                vector<lamp_mask_t> narrowed_button_effects;
                bool modified = true;
                while (modified) {
                    modified = false;
                    for (auto it = button_effects.begin();
                        it != button_effects.end();
                        ++it) {

                        if (*it == desired_lamps) {
                            // we don't need to test with anything but this map
                            // and the result will automatically be 1.

                            // clear the list of buttons and only leave the
                            // current one.
                            narrowed_button_effects.clear();
                            narrowed_button_effects.push_back(*it);
                            // exit the outer loop.
                            modified = false;
                            break;
                        } else {
                            auto desired_and = (desired_lamps & *it);
                            auto collateral_and = (collateral_lamps & *it);
                            if (desired_and != 0 || collateral_lamps != 0) {
                                // the button touches at least one of the
                                // desired lamps or the other lambs touched by
                                // previously-selected buttons.
                                collateral_lamps |= *it & ~desired_lamps;
                                narrowed_button_effects.push_back(*it);
                                button_effects.erase(it);
                                modified = true;
                                break;
                            }
                        }
                    }
                }

                if (button_effects.size() > 0) {
                    cout << "  optimized away " << button_effects.size()
                        << " button(s).\n";
                }

                auto r = find_minimum_presses_for_lamps(
                    0u,
                    desired_lamps,
                    passed_lamps,
                    narrowed_button_effects,
                    numeric_limits<size_t>::max());
                assert(passed_lamps.size() == 0);
                cout << r << endl;
                result += r;
                // we do not care about joltage in part 1.
                string remainder;
                getline(is, remainder);
                break;
            }
            assert(c == '(');
            vector<int> be;
            while (c != ')') {
                int n;
                is >> n >> c;
                be.push_back(n);
            }
            button_effects.push_back(encode_button_effects_for_lamps(be));
        }
    }
    throw new exception("should never reach this point");
}

static auto find_minimum_presses_for_joltage(
    vector<int>& current_joltage,
    const vector<int>& desired_joltage,
    const vector<vector<int>>& button_effects,
    unordered_map<vector<int>, size_t>& cache) {

    auto it = cache.find(current_joltage);
    if (it != cache.end()) {
        return it->second;
    }

    auto& cch = cache[current_joltage];
    cch = numeric_limits<size_t>::max();

    bool matched = true;
    for (auto i : views::iota(0uz, current_joltage.size())) {
        auto d = current_joltage[i] - desired_joltage[i];
        if (d < 0) {
            // we have lamps at a lower voltage than desired and we need to
            // press more buttons.
            matched = false;
        } else if (d > 0) {
            // this branch is a no-go since one lamp's joltage exceeded the
            // target one.
            return cch;
        }
    }

    if (matched) {
        cch = 0;
    } else {
        for (const auto& be : button_effects) {
            for (auto j : be) {
                current_joltage[j]++;
            }
            auto r = find_minimum_presses_for_joltage(
                current_joltage,
                desired_joltage,
                button_effects,
                cache);
            if (r < cch) {
                cch = r + 1;
            }
            for (auto j : be) {
                current_joltage[j]--;
            }
        }
    }
//    if (cch < numeric_limits<size_t>::max()) {
//        cout << "    ";
//        ranges::copy(current_joltage, ostream_iterator<int>(cout, ","));
//        cout << " -> " << cch << endl;
//    }
    return cch;
}

// https://adventofcode.com/2025/day/10#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts("part2");
    char c;
    auto result = 0LL;
    auto cn = -1;
    while (true) {
        cn++;
        is >> c;
        if (!is) {
            return result;
        }
        assert(c == '[');
        // we do not care about lamps in part 2.
        string lamps;
        getline(is, lamps, ']');

        vector<vector<int>> button_effects;
        while (true) {
            is >> c;
            if (c == '{') {
                vector<int> joltage;
                while (c != '}') {
                    int n;
                    is >> n >> c;
                    joltage.push_back(n);
                }

                vector<unordered_set<int>> affected_joltages(
                    joltage.size(), {});
                for (const auto& [i, be] : button_effects | views::enumerate) {
                    for (auto ji : be) {
                        affected_joltages[ji].insert(i);
                    }
                }

                auto r0 = 0uz;
                vector<int> buttons_to_remove;
                for (const auto& [ji, bis]
                    : affected_joltages | views::enumerate) {

                    if (bis.size() == 1) {
                        auto bi = *bis.cbegin();
                        auto d = joltage[ji];
                        r0 += d;
                        for (auto be : button_effects[bi]) {
                            joltage[be] -= d;
                        }
                        buttons_to_remove.push_back(bi);
                    }
                }
                ranges::sort(buttons_to_remove);
                ranges::reverse(buttons_to_remove);
                for (auto bi : buttons_to_remove) {
                    button_effects.erase(button_effects.begin() + bi);
                }
                cout << "  " << r0
                    << " / " << buttons_to_remove.size() << endl;
                vector<int> current_joltage(joltage.size(), 0);
                unordered_map<vector<int>, size_t> cache;
                auto r = r0 + find_minimum_presses_for_joltage(
                    current_joltage,
                    joltage,
                    button_effects,
                    cache
                );
                cout << cn << ": " << r << endl;
                result += r;
                break;
            }
            assert(c == '(');
            button_effects.emplace_back();
            while (c != ')') {
                int n;
                is >> n >> c;
                button_effects.back().push_back(n);
            }
        }
    }
    throw new exception("should never reach this point");
}

int main() {
    cout.imbue(locale(""));
    auto short_vector = R"([.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5})"sv;
    //cout << part1(ispanstream(short_vector)) << endl;
    //cout << part1(ifstream("input-vector.txt")) << endl;
    //cout << part2(ispanstream("[.##.] (2) (3) {0,1,0,1}"sv)) << endl;
    //cout << part2(ispanstream("[.##.] (3) {0,0,0,1}"sv)) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
