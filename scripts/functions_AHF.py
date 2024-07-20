
import numpy as np
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
    # Me quedo con una muesta de N periodos eliminando los extremos
    indices = get_zeros_indices(signal)

    signal_window = signal[indices[0]:indices[-1]]

    # Calcular la FFT de la señal     
    fft_signal = np.fft.fft(signal_window)

    # Calcular las frecuencias correspondientes a las muestras de la FFT
    frequencies = np.fft.fftfreq(len(fft_signal), 1/fs)

    #Elimino la mitad del esprectro asi como su continua
    fft_signal = fft_signal[1:int(len(fft_signal)/2)]
    frequencies = frequencies[1:len(fft_signal)]
    plt.plot
   
    # Encontrar el índice del pico más alto en la magnitud de la FFT (excluyendo la frecuencia DC)
    fundamental_index = np.argmax(np.abs(fft_signal[1:])) + 1 # El +1 representa la posicion que elimino al sacar la continua

    # Obtener la magnitud de la componente fundamental
    fundamental_magnitude = np.abs(fft_signal[fundamental_index])

    # Calcular la magnitud de las componentes armónicas
    harmonic_magnitudes = np.abs(fft_signal[fundamental_index +1:])

    # Calcular el THD
    thd = np.sqrt(np.sum(harmonic_magnitudes**2)) / fundamental_magnitude
    
    return thd


# def plot_signals(voltage_signal, current_signal, fs=1000):
#     # Calcular el tiempo para el eje x
#     duration = len(voltage_signal) / fs
#     t = np.linspace(0, duration, len(voltage_signal))
    
#     # Crear la figura y los ejes
#     plt.figure(figsize=(10, 6))
    
#     # Graficar la señal de tensión
#     plt.subplot(2, 1, 1)
#     plt.plot(t, voltage_signal, label='Tensión')
#     plt.xlabel('Tiempo [s]')
#     plt.ylabel('Amplitud')
#     plt.title('Señal de Tensión')
#     plt.grid(True)
#     plt.legend()
    
#     # Graficar la señal de corriente
#     plt.subplot(2, 1, 2)
#     plt.plot(t, current_signal, label='Corriente', color='orange')
#     plt.xlabel('Tiempo [s]')
#     plt.ylabel('Amplitud')
#     plt.title('Señal de Corriente')
#     plt.grid(True)
#     plt.legend()
    
#     # Ajustar el diseño y mostrar la gráfica
#     plt.tight_layout()
#     plt.show()

# Calculo de fp
def calculate_fp(tension, corriente, fs):
    """Funcion que calcula el factor de potencia de una señal de corriente y tension instantaneas

    Args:
        tension (_type_): _description_
        corriente (_type_): _description_
        fs (_type_): _description_
    """    
    # Para calcular Fp:
    # PF = RealP / S
    # S = Vrms * Irms
    # RealP= Valor medio de (V*I)

    #1 Calculo los valores RMS de tension y corriente para un ciclo.
    
    #1a elimino los ciclos incompletos y calculo valor RMS de tension.
    indices = get_zeros_indices(tension)
    _primer_cruce,_ultimo_cruce = indices[0], indices[-1]
    v_rms = calculate_rms(tension[_primer_cruce:_ultimo_cruce])

    #1b elimino los ciclos incompletos y calculo valor RMS de corriente.
    indices = get_zeros_indices(corriente)
    _primer_cruce,_ultimo_cruce = indices[0], indices[-1]
    i_rms = calculate_rms(corriente[_primer_cruce:_ultimo_cruce])

    #1c calculo la potencia reactiva
    p_aparente = i_rms * v_rms

    #2 Calculo el valor medio (potencia activa) de la linea
    p_activa = np.mean(tension*corriente)

    return p_activa / p_aparente


def calculate_rms(signal):
    """
    Calcula el valor RMS de una señal.

    Parámetros:
    signal (list o np.array): La señal a calcular su valor RMS.

    Retorna:
    float: El valor RMS de la señal.
    """
    # Convertir la señal a un array de NumPy si no lo es ya
    signal = np.array(signal)
    
    # Calcular el valor RMS
    rms_value = np.sqrt(np.mean(signal**2))
    
    return rms_value


def get_zeros_indices(signal):
    """funcion que recibe una señal como lista y detecta los cruces por cero ascendentes.

    Args:
        signal (_type_): señal a analizar

    Returns:
        _type_: indices de cruces por cero.
    """    
    indices = []
    previous = signal[0]
    for indice, value  in enumerate(signal):
        if previous <= 0 < value: # detecto un cruce por cero ascendente
            indices.append(indice)
        previous = value        
    
    return indices


## Funciones correccion
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import threading
import time
#Funciones para procesamiento y ploteo
def plot_signals(time,signal,correccion,signal_corregida,fs,axs,fig):
    clear_output(wait=True)
    axs[0].clear(),axs[1].clear(),axs[2].clear(),axs[3].clear()
        # Graficar Señal Medida
    axs[0].plot(time, signal, label='Señal Medida', color='b')
    axs[0].set_title('Señal Medida')
    axs[0].set_xlabel('Tiempo')
    axs[0].set_ylabel('Tensión')
    axs[0].grid(True)

    # Graficar Señal de Corrección
    axs[1].plot(time, correccion, label='Señal de Corrección', color='g')
    axs[1].set_title('Señal de Corrección')
    axs[1].set_xlabel('Tiempo')
    axs[1].set_ylabel('Tensión')
    axs[1].grid(True)

    # Graficar Señal Corregida
    axs[2].plot(time, signal_corregida, label='Señal Corregida', color='r')
    axs[2].set_title('Señal Corregida')
    axs[2].set_xlabel('Tiempo')
    axs[2].set_ylabel('Tensión')
    axs[2].grid(True)

    ## FFT
    fft_signal, freq = get_FFT(signal_corregida,fs)
    axs[3].plot(freq, fft_signal, label='Señal Corregida FFT', color='r')
    axs[3].set_title('Señal Corregida FFT')
    axs[3].set_xlabel('Freq')
    axs[3].set_ylabel('Tensión')
    axs[3].grid(True)
    # Ajustar el layout
    plt.tight_layout()
    
    # Mostrar la gráfica
    display(fig)


def get_signal(dev,fs): # Devuelve el valor medido en el canal 1
    dev.set_sampling(fs)  # maximo 40k a la entrada poner un filtro pasa bajos en 30k
    frames = dev.fetch()
    return frames.x() ,frames.y()[0] #tiempo,  Valores


def get_fundamental_FFT(values,time, fs,f_esperada):
   
    # Ventana para evitar leakege
    window_hamm = np.ones(len(values))#np.hamming(len(values)) # Le saque la ventana !!!!!
    _values = values * window_hamm

    # Calcular la FFT de la señal     
    fft_signal = np.fft.fft(_values)

    # Calcular las frecuencias correspondientes a las muestras de la FFT
    frequencies = np.fft.fftfreq(len(fft_signal), 1/fs)

    # normalizo la señal
    fft_signal = fft_signal/ len(fft_signal)

    #Elimino la mitad del esprectro 
    fft_signal = fft_signal[0:int(len(fft_signal)/2)]
    fft_signal = np.abs(fft_signal)
    freq = frequencies[0:len(fft_signal)]

    # Busco la componente fundamental medida, evito "suponer una frecuencia" ya que puede variar en la linea
    resolucion = freq[1]-freq[0] # Obtengo el delta entre mediciones de f
    indice = f_esperada / resolucion # Aproximo la cantidad de muestras hasta la fundamental teorica
    slice_amp = fft_signal[int(indice * 0.35):int(indice * 1.65)] # Busco a la fundamental en las cercania de la fc esperada
    slice_freq = freq[int(indice * 0.35):int(indice * 1.65)]
    indice =  np.argmax(slice_amp) # Encuentro el pico maximo
    fundamental_value = slice_amp[indice] 
    fundamental_freq = slice_freq[indice] # Frecuencia del pico maximo
    fundamental_signal =  fundamental_value*np.sin(time*fundamental_freq*2*np.pi)

    return fundamental_signal

def get_correccion(signal,fundamental):
        
    correccion = signal - fundamental ## Puedo hacer esto por que "values_i" es la señal medida con trigger, por lo que puedo ponerme en fase.

    corregida = signal - correccion

    return correccion,corregida

def get_FFT(values,fs):
     # Ventana para evitar leakege
    window_hamm = np.ones(len(values))#np.hamming(len(values))
    _values = values * window_hamm

    # Calcular la FFT de la señal     
    fft_signal = np.fft.fft(_values)

    # Calcular las frecuencias correspondientes a las muestras de la FFT
    frequencies = np.fft.fftfreq(len(fft_signal), 1/fs)

    # normalizo la señal
    fft_signal = fft_signal/ len(fft_signal)

    #Elimino la mitad del esprectro 
    fft_signal = fft_signal[0:int(len(fft_signal)/2)]
    fft_signal = np.abs(fft_signal)
    freq = frequencies[0:len(fft_signal)]

    return fft_signal,freq