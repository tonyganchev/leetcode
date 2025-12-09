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
        cout << label_ << ": " << duration << endl;
    }
private:
    const string label_;
    decltype(chrono::high_resolution_clock::now()) start_;
};
