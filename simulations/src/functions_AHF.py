
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def Generar_señal_linea(t, f0 = 50, cant_armonicos = 5, noise = False, noise_amp = 0.1  ):
    """Esta funcion permite generar una señal cualquiera con una fundamental en F0 y luego se le pueden agregar "cant_armonicos" armonicos a la señal.\n
    Si noise = True, se agrega ademas ruido a la señal con amplitud "noise_amp".

    Returns:
        _type_: devuelve la señal.
    """    
    N= len(t)
    noise_values = noise_amp * np.random.randn(N)
    signal =   np.sin(2 * np.pi *  f0 * t)
    for i in range(2,cant_armonicos):
        signal += (1 / i) *  np.sin(2 * np.pi * i * f0 * t) 
    if noise:
        signal += noise_values

    return signal


def calcular_thd(signal, fs):
    """
    Calcula la Distorsión Armónica Total (THD) de una señal.

    Args:
    signal (array_like): Señal de entrada.
    fs (float): Frecuencia de muestreo de la señal.

    Returns:
    float: THD de la señal...
    """
    # Calcular la FFT de la señal
    fft_signal = fft(signal)
    
    # Calcular las frecuencias correspondientes a las muestras de la FFT
    frequencies = fftfreq(len(signal), 1/fs)

    # Encontrar el índice del pico más alto en la magnitud de la FFT (excluyendo la frecuencia DC)
    fundamental_index = np.argmax(np.abs(fft_signal[1:])) + 1

    # Obtener la magnitud de la componente fundamental
    fundamental_magnitude = np.abs(fft_signal[fundamental_index])

    # Calcular la magnitud de las componentes armónicas
    harmonic_magnitudes = np.abs(fft_signal[fundamental_index*2:])

    # Calcular el THD
    thd = np.sqrt(np.sum(harmonic_magnitudes**2)) / fundamental_magnitude
    
    return thd


def plot_signals(voltage_signal, current_signal, fs=1000):
    # Calcular el tiempo para el eje x
    duration = len(voltage_signal) / fs
    t = np.linspace(0, duration, len(voltage_signal))
    
    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))
    
    # Graficar la señal de tensión
    plt.subplot(2, 1, 1)
    plt.plot(t, voltage_signal, label='Tensión')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title('Señal de Tensión')
    plt.grid(True)
    plt.legend()
    
    # Graficar la señal de corriente
    plt.subplot(2, 1, 2)
    plt.plot(t, current_signal, label='Corriente', color='orange')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title('Señal de Corriente')
    plt.grid(True)
    plt.legend()
    
    # Ajustar el diseño y mostrar la gráfica
    plt.tight_layout()
    plt.show()
