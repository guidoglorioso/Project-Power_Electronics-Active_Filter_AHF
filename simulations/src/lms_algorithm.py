import numpy as np
import matplotlib.pyplot as plt

# Parámetros
fs = 1000  # frecuencia de muestreo
f0 = 50    # frecuencia de la señal fundamental
N = 1000   # número de muestras
t = np.arange(N) / (fs)  # vector de tiempo

# Tension de linea
ruido_linea = 0.01 * np.random.randn(N)
tension_linea = np.sin(2 * np.pi * f0 * t) + ruido_linea
# Corriente de linea con armónicos
impedancia_linea = 2 # Ohm para la tension de linea
corriente_linea = tension_linea/impedancia_linea + 0.5 * np.sin(2 * np.pi * 2 * f0 * t) + 0.3 * np.sin(2 * np.pi * 3 * f0 * t) + 0.2 * np.sin(2 * np.pi * 4 * f0 * t)

# Añadir ruido
noise = 0.2 * np.random.randn(N)
corriente_linea_ruido = corriente_linea + noise

# Implementación del filtro LMS
def lms_filter(x, d, mu, M):
    N = len(x)
    w = np.zeros(M)
    y = np.zeros(N)
    e = np.zeros(N)

    for n in range(M, N):
        x_n = x[n:n-M:-1]
        y[n] = np.dot(w, x_n)
        e[n] = d[n] - y[n]
        w = w + 2 * mu * e[n] * x_n
    
    return y, e

# Parámetros del filtro LMS
mu = 0.01
M = 30

# Filtrado LMS
corriente_linea_ruido_corregida, error = lms_filter(corriente_linea_ruido, tension_linea, mu, M)

# Plotear señales
plt.figure(figsize=(14, 8))

plt.subplot(2, 1, 1)
plt.plot(t, tension_linea, label='Tension de linea')
plt.plot(t, corriente_linea_ruido, label='Corriente de linea con ruido')
plt.title('Tension de linea Vs Corriente de linea')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, corriente_linea_ruido_corregida, label='Corriente corregida')
plt.plot(t, tension_linea, label='Tension de linea')
#plt.plot(t, error, label='Señal de error')
plt.title('Tension de linea y corriente de filtrada')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()

plt.tight_layout()
plt.show()
