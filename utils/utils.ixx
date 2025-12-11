module;

export module utils;

import std;

using namespace std;

export class timer_scope {
public:
    timer_scope() : timer_scope("<no label>") { }
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
