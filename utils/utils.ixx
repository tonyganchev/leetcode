module;

export module utils;

import std;

using namespace std;

export class timer_scope {
public:
    timer_scope() : start_(chrono::high_resolution_clock::now()) {}
    ~timer_scope() {
        auto duration = chrono::high_resolution_clock::now() - start_;
        cout << "dur " << duration << endl;
    }
private:
    decltype(chrono::high_resolution_clock::now()) start_;
};
