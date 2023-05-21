import numpy as np
import matplotlib.pyplot as plt

# Definir los parámetros de la señal
duration = 2.0  # duración de la señal en segundos
fc = 6  # frecuencia de la portadora en Hz
bit_rate = 500  # tasa de bits en bps
bits_per_symbol = 3  # número de bits por símbolo
num_symbols = int(duration * bit_rate / bits_per_symbol)  # número total de símbolos

# Definir la constelación de 8-PSK
constellation = np.exp(1j * np.pi / 4 * np.arange(8))

# Generar la secuencia de bits aleatorios
bits = np.random.randint(0, 2, size=num_symbols * bits_per_symbol)

# Codificar los bits en símbolos
symbols = []
for i in range(0, len(bits), bits_per_symbol):
    index = int(''.join(map(str, bits[i:i+bits_per_symbol])), 2)
    symbols.append(constellation[index])

# Generar la señal modulada
t = np.linspace(0, duration, int(duration * bit_rate), endpoint=False)
signal = np.zeros_like(t, dtype=np.complex128)
for i, symbol in enumerate(symbols):
    start_index = i * int(bit_rate / bits_per_symbol)
    end_index = start_index + int(bit_rate / bits_per_symbol)
    signal[start_index:end_index] = symbol * np.exp(1j * 2 * np.pi * fc * t[start_index:end_index])

# Graficar la señal modulada
plt.figure(figsize=(20,5))
plt.plot(t, signal.real, color='r', label='Salida-8PSK') 
#plt.plot(t, signal.imag, color='b', label='Imag')
plt.title('Señal modulada 8-PSK')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.xlim(0, duration)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()














'''

import numpy as np
import matplotlib.pyplot as plt

# Definimos la función seno
def seno(x, A, f, phi):
    return A * np.sin(2 * np.pi * f * x + phi)

# Definimos la señal de salida para 8-PSK
num_symbols = 16
symbols = np.random.randint(8, size=num_symbols)
phases = symbols * (2 * np.pi / 8)
out_signal = np.zeros(num_symbols * 100)
for i in range(num_symbols):
    out_signal[i*100:(i+1)*100] = seno(np.linspace(i, i+1, 100), 1, 1, phases[i])

# Graficamos la señal de salida
plt.figure(figsize=(10, 5))
plt.plot(out_signal, linewidth=2, linestyle='-')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de salida 8-PSK')
plt.grid(True)
plt.xticks(np.arange(0, num_symbols*100, 100), symbols)
plt.show()
'''


