import numpy as np
import matplotlib.pyplot as plt


# Definir los parámetros de la señal
duration = 2.0  # duración de la señal en segundos
fc = 6  # frecuencia de la portadora en Hz
bit_rate = 5000  # tasa de bits en bps
bits_per_symbol = 4  # número de bits por símbolo
num_symbols = int(duration * bit_rate / bits_per_symbol)  # número total de símbolos

# Definir la constelación de 16-PSK
constellation = np.exp(1j * np.pi / 8 * np.arange(16))

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
plt.plot(t, signal.real, color='r', label='Salida-16PSK')
#plt.plot(t, signal.imag, color='b', label='Imag')
plt.title('Señal modulada 16-PSK')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.xlim(0, duration)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
