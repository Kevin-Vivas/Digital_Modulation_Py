import matplotlib.pyplot as plt
import numpy as np

class Modem:
    def __init__(self, M, constellation, name):
        self.M = M
        self.constellation = constellation
        self.name = name

class PSKModem(Modem):
    def __init__(self, M):        
        m = np.arange(0,M) #all information symbols m={0,1,...,M-1}
        I = 1/np.sqrt(2)*np.cos(m/M*2*np.pi)
        Q = 1/np.sqrt(2)*np.sin(m/M*2*np.pi)
        constellation = I + 1j*Q #reference constellation        
        Modem.__init__(self, M, constellation, name='PSK') #set the modem attributes

def plot_constellation(modem):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
    
    # Plot de la constelación con vectores
    ax1.axhline(0, color='k', linestyle='--')
    ax1.axvline(0, color='k', linestyle='--')
    ax1.set_xlabel('Real')
    ax1.set_ylabel('Imag')
    ax1.set_title(modem.name + ' Constellation')

 
    ax1.grid(True)
    
    for point in modem.constellation:
        ax1.arrow(0,0, point.real, point.imag, head_width=0.05, head_length=0.1, fc='b', ec='b')
    
    # Plot de la constelación con puntos
    ax2.scatter(modem.constellation.real, modem.constellation.imag, s=100, color='b')
    ax2.axhline(0, color='k', linestyle='--')
    ax2.axvline(0, color='k', linestyle='--')
    ax2.set_xlabel('Real')
    ax2.set_ylabel('Imag')
    ax2.set_title(modem.name + ' Constellation')
    ax2.grid(True)
    
    plt.show()

def main():
    M = 16
    psk_modem = PSKModem(M)
    plot_constellation(psk_modem)

if __name__ == '__main__':
    main()


