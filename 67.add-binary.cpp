/*
 * @lc app=leetcode id=67 lang=cpp
 *
 * [67] Add Binary
 */

#include <algorithm>
#include <string>

using namespace std;

// @lc code=start
class Solution {
public:
    string addBinary(string a, string b) {
        string r;
        if (a.length() > b.length()) {
            swap(a, b);
        }
        int carry = 0;
        auto i = 0;
        for (; i < a.length(); ++i) {
            auto ac = (int)(a[a.size() - i - 1] - '0');
            auto bc = (int)(b[b.size() - i - 1] - '0');
            auto s = ac + bc + carry;
            carry = s >> 1;
            s = s & 1;
            r.push_back((char)(s + '0'));
        }
        for (; i < b.length(); ++i) {
            auto bc = (int)(b[b.size() - i - 1] - '0');
            auto s = bc + carry;
            carry = s >> 1;
            s = s & 1;
            r.push_back((char)(s + '0'));
        }
        if (carry == 1) {
            r.push_back('1');
        }
        reverse(r.begin(), r.end());
        return r;
    }
};
// @lc code=end
