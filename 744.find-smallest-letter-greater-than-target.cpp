#include <vector>
#include <iostream>

using namespace std;

/*
 * @lc app=leetcode id=744 lang=cpp
 *
 * [744] Find Smallest Letter Greater Than Target
 */

// @lc code=start
class Solution {
public:
    char nextGreatestLetter(vector<char>& letters, char target) {
        bool found = false;
        char cc = '\0';
        for (auto c : letters) {
            if (c > target && (!found || cc - target > c - target)) {
                found = true;
                cc = c;
            }
        }
        return found ? cc : letters.front();
    }
};
// @lc code=end

int main() {
    vector<char> v { 'c', 'f', 'j' };
    cout << Solution().nextGreatestLetter(v, 'a') << endl;
}
