#include <iostream>
#include <cmath>


using namespace std;

double f_up(double x) {
    return min(x, -x + 6);
}

double f_down() {
    return 2; 
}

double simpson_rule(double a, double b, int n) {
    if (n % 2 != 0) {
        n++; 
    }
    double h = (b - a) / n;
    double sum = f_up(a) - f_down(); 
    for (int i = 1; i < n; i++) {
        double x = a + i * h;
        if (i % 2 == 0) {
            sum += 2 * (f_up(x) - f_down());
        }
        else {
            sum += 4 * (f_up(x) - f_down());
        }
    }
    return (h / 3) * sum;
}

int main() {
    setlocale(LC_ALL, "Russian");
    double a = 2; 
    double b = 4; 
    int n = 2;
    double area = simpson_rule(a, b, n);
    cout << "Площадь фигуры: " << area << endl;
    return 0;
}
