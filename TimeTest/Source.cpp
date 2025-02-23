#include <iostream>
#include <map>
#include <set>
#include <chrono>
#include <cmath>
#include <random>
using namespace std;

template <typename Size>
long long Set_time_measure(Size& set, int size) {
    auto start_time = chrono::high_resolution_clock::now();
    for (int i = 1; i < size + 1; i++) {
        set.insert(i);
    }
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time);
    return duration.count();
}

int main() {
    set<int> ULTIMATE_SET;
    for (int i = 1; i < 9; i++) {
        int len = pow(10, i);
        cout << len << " size " << i << " i " << endl;
        cout << Set_time_measure(ULTIMATE_SET, len) << "mks, " << len << " operations" << endl;
    }
    set<int> GIGA_SET;
    cout << Set_time_measure(GIGA_SET, 125000000) << "mks, 125000000 operations" << endl;
    cout << Set_time_measure(GIGA_SET, 150000000) << "mks, 150000000 operations" << endl;
    return 0;
}
