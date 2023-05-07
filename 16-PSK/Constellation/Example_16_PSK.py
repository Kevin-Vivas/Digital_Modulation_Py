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
    plt.scatter(modem.constellation.real, modem.constellation.imag, s=100, color='b')
    plt.axhline(0, color='k', linestyle='--')
    plt.axvline(0, color='k', linestyle='--')
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.title(modem.name + ' Constellation')
    plt.grid(True)
    plt.show()

def main():
    M = 16
    psk_modem = PSKModem(M)
    plot_constellation(psk_modem)

if __name__ == '__main__':
    main()

