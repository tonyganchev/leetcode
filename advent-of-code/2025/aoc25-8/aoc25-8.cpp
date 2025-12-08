import std;
import utils;

using namespace std;

using coord_t = long long;

struct point {
    coord_t x, y, z;
};

template <typename Stream>
Stream& operator >>(Stream& is, point& pt) {
    char c;
    is >> pt.x >> c >> pt.y >> c >> pt.z;
    return is;
}

long long calc_dist_sq(
    const vector<point> points,
    const size_t from,
    const size_t to) {

    auto dx = points[from].x - points[to].x;
    auto dy = points[from].y - points[to].y;
    auto dz = points[from].z - points[to].z;
    return dx * dx + dy * dy + dz * dz;
}

struct point_pair {
    size_t from;
    size_t to;
    coord_t dist_sq;

    bool operator >(const point_pair& other) const {
        return dist_sq > other.dist_sq;
    }

    point_pair(const point_pair&) = default;
    point_pair(const vector<point>& pts, const size_t& f, const size_t& t)
        : from(f), to(t), dist_sq(calc_dist_sq(pts, f, t)) {
    }
    point_pair& operator =(const point_pair&) = default;
};

struct fuses {
    
    vector<point> points;

    priority_queue<
        point_pair,
        vector<point_pair>,
        greater<point_pair>
    > distances;
    
    size_t cur_circ;
    
    unordered_map<long long, long long> circuit_of;
    
    unordered_map<long long, unordered_set<long long>> circuit_points;
    
    fuses() : cur_circ(1z) {}

    void connect(const point_pair& pp) {
        const auto& [from, to, _] = pp;
        auto& new_circuit = circuit_of[from];
        if (new_circuit == 0) {
            new_circuit = cur_circ++;
            circuit_points[new_circuit].insert(from);
        }
        const auto old_circuit = circuit_of[to];
        if (old_circuit != new_circuit) {
            for (auto& pt : circuit_points[old_circuit]) {
                circuit_of[pt] = new_circuit;
                circuit_points[new_circuit].insert(pt);
            }
            circuit_points.erase(old_circuit);
            circuit_of[to] = new_circuit;
            circuit_points[new_circuit].insert(to);
        }
    }

    bool all_connected() const {
        return circuit_points.size() == 1
            && circuit_points.cbegin()->second.size() == points.size();
    }
};

template <typename Stream>
Stream& operator >>(Stream& is, fuses& f) {
    point pt;
    while (is >> pt) {
        f.points.push_back(pt);
    }
    for (auto i : views::iota(0uz, f.points.size() - 1)) {
        for (auto j : views::iota(i + 1, f.points.size())) {
            f.distances.emplace(f.points, i, j);
        }
    }
    return is;
}

// https://adventofcode.com/2025/day/8
template <typename Stream>
static auto part1(Stream is, size_t pair_count) {
    timer_scope ts("part1");
    fuses f;
    is >> f;

    for (auto i : views::iota(0uz, min(pair_count, f.distances.size()))) {
        const auto& dist = f.distances.top();
        f.connect(dist);
        f.distances.pop();
    }

    auto comp_circ_sizes = [&f](const long long l, const long long r) {
        return f.circuit_points[l].size() < f.circuit_points[r].size();
        };
    const auto circuit_ids = f.circuit_points | views::keys;
    priority_queue<
        long long,
        vector<long long>,
        decltype(comp_circ_sizes)
    > largest_circuits(
        circuit_ids.cbegin(), circuit_ids.cend(), comp_circ_sizes);

    auto result = 1LL;
    for (auto i : views::iota(0uz, min(3uz, largest_circuits.size()))) {
        result *= f.circuit_points[largest_circuits.top()].size();
        largest_circuits.pop();
    }
    return result;
}

// https://adventofcode.com/2025/day/8#part2
template <typename Stream>
static auto part2(Stream is) {
    timer_scope ts("part2");
    fuses f;
    is >> f;

    for (auto i : views::iota(0uz, f.distances.size())) {
        const auto& dist = f.distances.top();
        f.connect(dist);
        if (f.all_connected()) {
            return f.points[dist.from].x * f.points[dist.to].x;
        }
        f.distances.pop();
    }

    return 0LL;
}

int main() {
    auto short_vector = R"(162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689)"sv;
    cout << part1(ispanstream(short_vector), 10) << endl;
    cout << part1(ifstream("input-vector.txt"), 1000) << endl;
    cout << part2(ispanstream(short_vector)) << endl;
    cout << part2(ifstream("input-vector.txt")) << endl;
    return 0;
}
