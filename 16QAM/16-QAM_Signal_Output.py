import numpy as np
import matplotlib.pyplot as plt

# Definición de los puntos de inicio y final para cada rango de valores de x
inicio = 0
final = 2*np.pi
x = []
for _ in range(8):
    x.append(np.arange(inicio, final, 0.1))
    inicio += 6.3
    final += 2*np.pi

# Concatenación de todos los valores de x en un solo arreglo
a = []
for i in range(8):
    a = np.concatenate((a, x[i]))

# Definición de las fases y amplitudes para cada onda sinusoidal
phase = [-135, -135, -45, -45, 135, 135, 45, 45]
amplitud = [0.765, 1.048, 0.765, 1.048, 0.765, 1.048, 0.765, 1.048]

# Cálculo de las coordenadas y para cada onda sinusoidal
y = []
for i in range(8):
    y.append(amplitud[i] * (np.sin(x[i] + phase[i])))

# Configuración de la figura y trazado de las ondas sinusoidales
plt.figure(figsize=(20, 6))
for i in range(8):
    plt.plot(x[i], y[i])

plt.grid(axis='both')
plt.title('16-QAM_Signal_Output')
plt.show()



