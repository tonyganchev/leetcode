module;

export module utils;

import std;

using namespace std;

export template <typename T>
concept ConstMapLike = requires(const T m, const typename T::key_type& k) {
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

export string_view trim(string_view sv) noexcept {
    // Find the first non-whitespace character
    const auto first = find_if_not(sv.begin(), sv.end(), static_cast<int (*)(int)>(&isspace));
    // If all characters are whitespace, return an empty view
    if (first == sv.end()) {
        return {};
    }

    // Find the last non-whitespace character (search from the end)
    const auto last = find_if_not(sv.rbegin(), sv.rend(), static_cast<int (*)(int)>(&isspace)).base();

    // Calculate the new start position and length
    const auto new_start = distance(sv.begin(), first);
    const auto new_len = distance(first, last);

    return sv.substr(new_start, new_len);
}
