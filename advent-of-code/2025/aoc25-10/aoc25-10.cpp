#include <cassert>
#include <Eigen/Dense>

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

static const double epsilon = 1e-9;

// Function to check if a double is effectively an integer within tolerance
bool is_effectively_integer(double val) {
    return std::abs(val - std::round(val)) < epsilon;
}

// Function that recursively explores parameter combinations
void find_optimal_solution_recursive(
    int param_index,
    int num_params,
    Eigen::VectorXd current_params_d,
    const Eigen::VectorXd& particular_solution,
    const Eigen::MatrixXd& kernel,
    double& best_sum_out,
    Eigen::VectorXd& best_solution_out_d,
    bool& found_solution_out
) {
    if (param_index == num_params) {
        Eigen::VectorXd current_x = particular_solution;
        for (int i = 0; i < num_params; ++i) {
            current_x += current_params_d[i] * kernel.col(i);
        }

        bool all_valid = true;
        for (int i = 0; i < current_x.size(); ++i) {
            double val = current_x[i];
            if (val < -epsilon || !is_effectively_integer(val)) {
                all_valid = false;
                break;
            }
        }

        if (all_valid) {
            double current_sum = current_x.sum();
            if (current_sum < best_sum_out) {
                best_sum_out = current_sum;
                best_solution_out_d = current_x;
                found_solution_out = true;
            }
        }
        return;
    }

    int lower_bound = 0;
    // Determined based on max input joltage.
    int upper_bound = 266;

    for (int p_val = lower_bound; p_val <= upper_bound; ++p_val) {
        current_params_d[param_index] = static_cast<double>(p_val);
        find_optimal_solution_recursive(param_index + 1, num_params, current_params_d,
            particular_solution, kernel,
            best_sum_out, best_solution_out_d, found_solution_out);
    }
}

static auto run_simulation(const string line) {
    auto raw_items = string_view(line) | views::split(' ');
    vector<unordered_set<int>> button_effects;
    vector<int> joltage;
    for (const auto& item : raw_items) {
        if (item.front() == '[') {
            // we do not care about lamps in part 2.
            continue;
        }

        if (item.front() == '(') {
            ispanstream is(item);
            char c;
            is >> c;
            assert(c == '(');
            button_effects.emplace_back();
            int n;
            while (is >> n >> c) {
                button_effects.back().insert(n);
            }
        } else {
            ispanstream is(item);
            char c;
            is >> c;
            int n;
            while (is >> n >> c) {
                joltage.push_back(n);
            }
        }
    }

    Eigen::MatrixXd left(joltage.size(), button_effects.size());
    Eigen::VectorXd right(joltage.size());

    for (const auto [ji, jv] : joltage | views::enumerate) {
        for (const auto& [bi, bv] : button_effects | views::enumerate) {
            left(ji, bi) = (bv.contains(ji) ? 1 : 0);
        }
        right[ji] = jv;
    }

    auto lu_decomp = left.fullPivLu();

    if (!lu_decomp.isInvertible())
    {
        auto rank = lu_decomp.rank();
        auto nullity = button_effects.size() - rank;
        
        auto kernel = lu_decomp.kernel();
        
        auto particular_solution = lu_decomp.solve(right);
        
        int num_parameters = kernel.cols();
        Eigen::VectorXd initial_params = Eigen::VectorXd::Zero(num_parameters);

        double best_sum = std::numeric_limits<double>::max();
        Eigen::VectorXd final_best_solution_d;
        bool found_solution = false;

        find_optimal_solution_recursive(0, num_parameters, initial_params,
            particular_solution, kernel,
            best_sum, final_best_solution_d, found_solution);

        if (found_solution) {
            return best_sum;
        }
        
        return 0.0 + numeric_limits<size_t>::max();

    } else {
        Eigen::VectorXd coeffs = lu_decomp.solve(right);
        assert(coeffs.size() == button_effects.size());

        return coeffs.sum();
    }
}

// https://adventofcode.com/2025/day/10#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts("part2");
    auto result = 0.0;
    unordered_map<int, future<double>> tasks;
    auto pool_size = thread::hardware_concurrency() - 1u;
    string s;
    int id = 0;
    while (getline(is, s)) {
        while (tasks.size() == pool_size) {
            for (auto& [id, f] : tasks) {
                if (f.wait_for(0s) == future_status::ready) {
                    auto r = f.get();
                    result += r;
                    cout << id << ": " << r << endl;
                    tasks.erase(id);
                    break;
                }
            }
        }
        tasks[++id] = async(run_simulation, s);
    }
    for (auto& [id, f] : tasks) {
        auto r = f.get();
        result += r;
        cout << id << ": " << r << endl;
    }
    return result;
}

int main() {
    auto short_vector = R"([.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7};
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5})"sv;
    cout << part1(ispanstream(short_vector)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    //cout << part2(ispanstream("[.##.] (2) (3) {0,1,0,1}"sv)) << endl;
    //cout << part2(ispanstream("[.##.] (2) (3) {0,0,1,1}"sv)) << endl;
    //cout << part2(ispanstream("[.##.] (0) (1) (3) (3) {0,0,0,3}"sv)) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
