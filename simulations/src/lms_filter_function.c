// lms_filter.c
#include <stdio.h>

__declspec(dllexport) void lms_filter(double* x, double* d, double* y, double* e, double* w, int N, int M, double mu) {
    for (int n = M; n < N; n++) {
        double y_n = 0.0;
        for (int i = 0; i < M; i++) {
            y_n += w[i] * x[n-i];
        }
        y[n] = y_n;
        e[n] = d[n] - y[n];
        for (int i = 0; i < M; i++) {
            w[i] += 2 * mu * e[n] * x[n-i];
        }
    }
}
