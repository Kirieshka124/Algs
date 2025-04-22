#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>

std::vector<int> array;
const int ARRAY_SIZE = 100000;

void generateArray() {
    array.clear();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(10, 1000000);

    for (int i = 0; i < ARRAY_SIZE; i++) {
        array.push_back(dist(gen));
    }
}

template <typename Func, typename... Args>
auto measure_execution_time(Func&& func, Args&&... args) {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::forward<Func>(func)(std::forward<Args>(args)...);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    return duration.count();
}


void BubbleSort(std::vector<int>& array) {
    int n = array.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                std::swap(array[j], array[j + 1]);
            }
        }
    }
}


void RadixSort(std::vector<int>& array) {
    if (array.empty()) return;
    int max_num = *std::max_element(array.begin(), array.end());
    for (int exp = 1; max_num / exp > 0; exp *= 10) {
        std::vector<int> output(array.size());
        std::vector<int> count(10, 0);
        for (int i = 0; i < array.size(); i++)
            count[(array[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++)
            count[i] += count[i - 1];
        for (int i = array.size() - 1; i >= 0; i--) {
            output[count[(array[i] / exp) % 10] - 1] = array[i];
            count[(array[i] / exp) % 10]--;
        }
        for (int i = 0; i < array.size(); i++)
            array[i] = output[i];
    }
}

int QuickSortHelp(std::vector<int>& array, int low, int high) {
    int pivot = array[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (array[j] < pivot) {
            i++;
            std::swap(array[i], array[j]);
        }
    }
    std::swap(array[i + 1], array[high]);
    return (i + 1);
}

void QuickSort(std::vector<int>& array, int low, int high) {
    if (low < high) {
        int pi = QuickSortHelp(array, low, high);

        QuickSort(array, low, pi - 1);
        QuickSort(array, pi + 1, high);
    }
}

int main() {
    setlocale(LC_ALL, "ru");

    generateArray();
    double BubbleSort_Time = measure_execution_time(BubbleSort, array);

    generateArray();
    double RadixSort_Time = measure_execution_time(RadixSort, array);

    generateArray();
    double QuickSort_Time = measure_execution_time(QuickSort, array, 0, array.size() - 1);

    std::cout << "Время выполнения сортировки пузырьком: " << BubbleSort_Time << "мс" << std::endl;
    std::cout << "Время выполнения поразрядной сортировки: " << RadixSort_Time << "мс" << std::endl;
    std::cout << "Время выполнения быстрой сортировки: " << QuickSort_Time << "мс" << std::endl;

    return 0;
}