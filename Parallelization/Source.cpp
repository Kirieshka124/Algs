#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
#include <thread>

std::vector<int> array;


void generateArray(int ARRAY_SIZE) {
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

void QuickSort_using_threads(std::vector<int>& array, int num_threads)
{
    int size = array.size();
    int partSize = size / num_threads;
    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        int start = i * partSize;
        int end;
        if (i == num_threads - 1) {
            end = size - 1;
        }
        else {
            end = start + partSize - 1;
        }
        threads.emplace_back(QuickSort, std::ref(array), start, end);
    }

    for (auto& thread : threads) {
        thread.join();
    }

    int step = partSize;
    while (step < size) {
        for (int i = 0; i < size - step; i += 2 * step) {
            int left = i;
            int mid = i + step;
            int right = std::min(i + 2 * step, size);

            std::inplace_merge(array.begin() + left, array.begin() + mid, array.begin() + right);
        }
        step *= 2;
    }
}

int main()
{
    setlocale(LC_ALL, "ru");

    int array_size = 1000000;

    generateArray(array_size);
    double QuickSort_threading_2 = measure_execution_time(QuickSort_using_threads, array, 2);
    std::cout << "Быстрая сортировка 2 потока " << QuickSort_threading_2 << "мс" << std::endl;

    generateArray(array_size);
    double QuickSort_threading_4 = measure_execution_time(QuickSort_using_threads, array, 4);
    std::cout << "Быстрая сортировка 4 потока " << QuickSort_threading_4 << "мс" << std::endl;

    generateArray(array_size);
    double QuickSort_threading_8 = measure_execution_time(QuickSort_using_threads, array, 8);
    std::cout << "Быстрая сортировка 8 потоков " << QuickSort_threading_8 << "мс" << std::endl;

}