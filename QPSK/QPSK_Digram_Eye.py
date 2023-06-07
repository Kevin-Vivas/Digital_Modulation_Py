import numpy as np
import matplotlib.pyplot as plt
from passband_modulations import qpsk_mod, piBy4_dqpsk_mod
from raisedCosineDesign import raisedCosineDesign

N = 1000 # Número de símbolos a transmitir, mantenerlo pequeño y adecuado
fc = 10; L = 8 # Frecuencia portadora y factor de sobremuestreo
a = np.random.randint(2, size=N) # Símbolos aleatorios uniformes de 0's y 1's

# Modula los símbolos fuente utilizando QPSK y pi/4-DQPSK
qpsk_result = qpsk_mod(a, fc, L)
piby4qpsk_result = piBy4_dqpsk_mod(a, fc, L)

# Forma de pulso las formas de onda moduladas mediante la convolución con el filtro RC
alpha = 0.3; span = 10 # Alpha del filtro RC y duración en símbolos
b = raisedCosineDesign(alpha, span, L) # Generación de la forma de onda de pulso RC
iRC_qpsk = np.convolve(qpsk_result['I(t)'], b, mode='valid') # RC - QPSK I(t)
qRC_qpsk = np.convolve(qpsk_result['Q(t)'], b, mode='valid') # RC - QPSK Q(t)
iRC_piby4qpsk = np.convolve(piby4qpsk_result['U(t)'], b, mode='valid') # pi/4-QPSK I
qRC_piby4qpsk = np.convolve(piby4qpsk_result['V(t)'], b, mode='valid') # pi/4-QPSK Q

# Graficar los resultados
fig, axs = plt.subplots(1, 2)
axs[0].plot(iRC_qpsk, qRC_qpsk) # RC en forma de QPSK
axs[1].plot(iRC_piby4qpsk, qRC_piby4qpsk) # RC en forma de pi/4-QPSK
axs[0].set_title(r'Digram_Eye_QPSK, RC $\alpha$=' + str(alpha))
axs[0].set_xlabel('I(t)'); axs[0].set_ylabel('Q(t)');
axs[1].set_title(r'$\pi$/4 - Digram_Eye_QPSK, RC $\alpha$=' + str(alpha))
axs[1].set_xlabel('I(t)'); axs[1].set_ylabel('Q(t)');

plt.show()



