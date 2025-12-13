module;

export module utils;

import std;

using namespace std;

export class timer_scope {
public:
    timer_scope() : timer_scope("<no label>") {}
    timer_scope(const char* label)
        : label_(label), start_(chrono::high_resolution_clock::now()) {

        cout << label_ << " start ..." << endl;
    }
    ~timer_scope() {
        auto duration = chrono::high_resolution_clock::now() - start_;
        cout << label_ << ": "
            << chrono::duration_cast<chrono::microseconds>(duration)
            << endl;
    }
private:
    const string label_;
    decltype(chrono::high_resolution_clock::now()) start_;
};

export template <typename T>
concept ConstMapLike = requires(const T m, const typename T::key_type & k) {
    typename T::key_type;
    typename T::mapped_type;
    { m.find(k) } -> same_as<typename T::const_iterator>;
    { m.end() } -> same_as<typename T::const_iterator>;
};

export template <ConstMapLike MapContainer>
auto try_get(
    const MapContainer& container,
    const typename MapContainer::key_type& key,
    const typename MapContainer::mapped_type& default_value) {
    auto it = container.find(key);
    if (it == container.end()) {
        return default_value;
    }
    return it->second;
}

template <typename T>
concept non_void = !is_void_v<T>;

template <typename F>
concept line_computer =
    invocable<F, string>
    && non_void<invoke_result_t<F, string>>
    && totally_ordered<invoke_result_t<F, string>>;

export template <typename Stream, line_computer Function>
auto solve_in_parallel(Stream& is, Function& func) {
    using return_type = invoke_result_t<Function, string>;
    return_type result = static_cast<return_type>(0);
    unordered_map<int, future<return_type>> tasks;
    auto pool_size = thread::hardware_concurrency() - 1u;
    string line;
    int id = 0;
    while (getline(is, line)) {
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
        tasks[++id] = async(func, line);
    }
    for (auto& [id, f] : tasks) {
        auto r = f.get();
        result += r;
        cout << id << ": " << r << endl;
    }
    return result;
}
