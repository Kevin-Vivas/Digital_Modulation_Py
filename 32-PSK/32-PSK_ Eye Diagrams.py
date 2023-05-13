import numpy as np
import matplotlib.pyplot as plt

# Definir las constantes
M =  32  # Número de símbolos en la constelación
N = 20 # Número de muestras
fc = 100 # Frecuencia de la portadora

# Definir los símbolos de la constelación
constelacion = np.exp(1j*2*np.pi*np.arange(M)/M)

# Generar los datos de prueba
bits = np.random.randint(0, M, size=N)
simbolos = constelacion[bits]
t = np.arange(N)
portadora = np.sin(2*np.pi*fc*t/N)
senal_modulada = np.real(simbolos*np.exp(1j*2*np.pi*fc*t/N))
'''
# Graficar el diagrama de constelación
plt.subplot(2,2,1)
plt.plot(np.real(simbolos), np.imag(simbolos), 'o')
plt.title('Diagrama de constelación')
'''
# Graficar el diagrama de ojo
plt.subplot()
for i in range(M):
    plt.plot(t, np.real(senal_modulada*(constelacion[i]/np.abs(constelacion[i]))))
plt.title('Diagrama de ojo')

# Graficar la señal modulada
'''
plt.subplot(2,1,2)
plt.plot(t, senal_modulada*portadora)
plt.title('Señal modulada')
plt.xlabel('Tiempo')
'''
plt.show()