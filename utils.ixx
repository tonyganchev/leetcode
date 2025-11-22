module;

export module utils;

import std;

export template <typename T>
concept ConstMapLike = requires(const T m, const typename T::key_type& k) {
    typename T::key_type;
    typename T::mapped_type;
    { m.find(k) } -> std::same_as<typename T::const_iterator>;
    { m.end() } -> std::same_as<typename T::const_iterator>;
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
