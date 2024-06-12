#include <iostream>

// c++ -std=c++20 -Ofast -march=native predictions.cpp -o predictions && ./predictions
const long LOOPS = 10'000'000;

int main() {
    std::srand(std::time(nullptr));  // Init rand

    long totalRuns = 0;
    int runs;

    for (int i = 0; i < LOOPS; i++) {
        runs = 1;

        while (std::rand() % 3'000 + 1 != 1) {
            runs++;
        }

        totalRuns += runs;
    }

    std::cout << "Total runs: " << totalRuns << std::endl;
    std::cout << "Mean: " << totalRuns / LOOPS << std::endl;
}
