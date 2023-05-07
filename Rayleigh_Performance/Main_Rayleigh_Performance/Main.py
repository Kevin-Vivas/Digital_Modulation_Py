import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from Modem_Uno import PSKModem
from channels import awgn, rayleighFading
from ErrorRates import ser_rayleigh

#---------Input Fields------------------------
nSym = 10**6 # Number of symbols to transmit
EbN0dBs = np.arange(start=-4, stop=12, step=2) # Eb/N0 range in dB for simulation
arrayOfM = [4, 8, 16, 32] # array of M values to simulate

colors = plt.cm.jet(np.linspace(0, 1, len(arrayOfM))) # colormap
fig, ax = plt.subplots(nrows=1, ncols=1)

for i, M in enumerate(arrayOfM):
    k = np.log2(M)
    EsN0dBs = 10*np.log10(k)+EbN0dBs # EsN0dB calculation
    SER_sim = np.zeros(len(EbN0dBs)) # simulated Symbol error rates
    # uniform random symbols from 0 to M-1
    inputSyms = np.random.randint(low=0, high=M, size=nSym)
    modem = PSKModem(M) # choose a PSK modem
    modulatedSyms = modem.modulate(inputSyms) # modulate

    for j, EsN0dB in enumerate(EsN0dBs):
        h_abs = rayleighFading(nSym) # Rayleigh flat fading samples
        hs = h_abs*modulatedSyms # fading effect on modulated symbols
        receivedSyms = awgn(hs, EsN0dB) # add AWGN noise
        y = receivedSyms/h_abs # decision vector
        detectedSyms = modem.demodulate(y) # demodulate (Refer Chapter 3)
        SER_sim[j] = np.sum(detectedSyms != inputSyms)/nSym
        SER_theory = ser_rayleigh(EbN0dBs, 'psk', M) # theory SER
    ax.semilogy(EbN0dBs, SER_sim, color=colors[i], marker='o', linestyle='', label=' '+str(M)+'-PSK')
    ax.semilogy(EbN0dBs, SER_theory, color=colors[i], linestyle='-', label=''+str(M)+'-PSK')

ax.set_xlabel('Eb/N0(dB)'); ax.set_ylabel('Symbol Error Rate (Ps)')
ax.set_title('Probability of Symbol Error for M- PSK')
ax.legend()
plt.show()
