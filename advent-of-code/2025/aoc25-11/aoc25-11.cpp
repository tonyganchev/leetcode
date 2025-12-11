#include <cassert>

import std;
import utils;

using namespace std;

template <typename Stream>
Stream& operator >>(
    Stream& is,
    unordered_map<string, unordered_map<string, size_t>>& outputs) {

    string s;
    string device;
    while (is >> s) {
        if (s.back() == ':') {
            device = s.substr(0, s.size() - 1);
        } else {
            outputs[device].emplace(move(s), 1);
        }
    }
    return is;
}

static auto simplify(
    unordered_map<string, unordered_map<string, size_t>>& outputs,
    const unordered_set<string>& preserved_nodes) {

    auto optimizations = 0uz;
    bool changes_made = true;
    while (changes_made) {
        changes_made = false;
        vector<string> nodes_to_delete;
        for (const auto& [from_node, to_nodes] : outputs) {
            if (!preserved_nodes.contains(from_node)) {
                for (auto& [fn, tn] : outputs) {
                    auto jt = tn.find(from_node);
                    if (jt != tn.end()) {
                        for (const auto& [to_node, power] : to_nodes) {
                            tn[to_node] += jt->second * power;
                        }
                        tn.erase(jt);
                    }
                }
                optimizations++;
                changes_made = true;
                nodes_to_delete.push_back(from_node);
            }
        }
        for (const auto& n : nodes_to_delete) {
            outputs.erase(n);
        }
    }
    cout << "Optimized away " << optimizations << " node(s).\n";
}

static auto paths(
    const unordered_map<string, unordered_map<string, size_t>>& outputs,
    const string& current_device,
    const string& target_device,
    const unordered_map<string, bool>& required_nodes) {

    if (current_device == target_device) {
        return 1uz;
    }

    auto result = 0uz;
    auto it = outputs.find(current_device);
    if (it == outputs.cend()) {
        return 0uz;
    }
    for (const auto& [out, ps] : it->second) {
        auto jt = required_nodes.find(out);
        if (jt == required_nodes.cend() || jt->second) {
            result += ps * paths(outputs, out, target_device, required_nodes);
        }
    }
    return result;
}

// https://adventofcode.com/2025/day/10
template <typename Stream>
static auto part1(Stream is) {
    timer_scope ts("part1");
    unordered_map<string, unordered_map<string, size_t>> outputs;
    is >> outputs;
    unordered_set<string> preserved_nodes = { "you"s, "out"s };
    simplify(outputs, preserved_nodes);
    unordered_map<string, bool> no_required_nodes;
    return outputs["you"s]["out"s];
}

// https://adventofcode.com/2025/day/11#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts("part2");
    unordered_map<string, unordered_map<string, size_t>> outputs;
    is >> outputs;
    unordered_set<string> preserved_nodes = { "svr"s, "out"s, "fft"s, "dac"s };
    simplify(outputs, preserved_nodes);
    unordered_map<string, bool> no_dac_out = {
        { "fft"s, true },
        { "dac"s, false },
        { "out"s, false }
    };
    unordered_map<string, bool> no_fft_out = {
        { "fft"s, false },
        { "dac"s, true },
        { "out"s, false }
    };
    unordered_map<string, bool> no_dac_fft = {
        { "fft"s, false },
        { "dac"s, false },
        { "out"s, true }
    };
    auto svr_to_fft = outputs["svr"s]["fft"s];
    auto svr_to_dac = outputs["svr"s]["dac"s];
    auto dac_to_fft = outputs["dac"s]["fft"s];
    auto dac_to_out = outputs["dac"s]["out"s];
    auto fft_to_dac = outputs["fft"s]["dac"s];
    auto fft_to_out = outputs["fft"s]["out"s];

    return svr_to_fft * fft_to_dac * dac_to_out
        + svr_to_dac * dac_to_fft * fft_to_out;
}

int main() {
    auto short_vector1 = R"(aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out)"sv;
    cout << part1(ispanstream(short_vector1)) << endl;
    cout << part1(ifstream("input-vector.txt")) << endl;
    auto short_vector2 = R"(svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out)"sv;
    cout << part2(ispanstream(short_vector2)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
