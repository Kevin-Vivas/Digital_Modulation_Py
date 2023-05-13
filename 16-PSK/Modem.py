import matplotlib.pyplot as plt
import numpy as np
import abc
class Modem:
    __metadata__ = abc.ABCMeta
    # Base class: Modem
    # Attribute definitions:
    #    self.M : number of points in the MPSK constellation
    #    self.name: name of the modem : PSK, QAM, PAM, FSK
    #    self.constellation : reference constellation
    #    self.coherence : only for 'coherent' or 'noncoherent' FSK
    def __init__(self,M,constellation,name,coherence=None): #constructor
        if (M<2) or ((M & (M -1))!=0): #if M not a power of 2
            raise ValueError('M should be a power of 2')
        if name.lower()=='fsk':
            if (coherence.lower()=='coherent') or (coherence.lower()=='noncoherent'):
                self.coherence = coherence
            else:
                raise ValueError('Coherence must be \'coherent\' or \'noncoherent\'')
        else:
            self.coherence = None
        self.M = M # number of points in the constellation
        self.name = name # name of the modem : PSK, QAM, PAM, FSK
        self.constellation = constellation # reference constellation
    
    def plotConstellation(self):
        """
        Plot the reference constellation points for the selected modem
        """
        from math import log2
        if self.name.lower()=='fsk':
            return 0 # FSK is multi-dimensional difficult to visualize 
        
        fig, axs = plt.subplots(1, 1)
        axs.plot(np.real(self.constellation),np.imag(self.constellation),'o')        
        for i in range(0,self.M):
            axs.annotate("{0:0{1}b}".format(i,int(log2(self.M))), (np.real(self.constellation[i]),np.imag(self.constellation[i])))
        
        axs.set_title('Constellation');
        axs.set_xlabel('I');axs.set_ylabel('Q');fig.show()
    
    def modulate(self,inputSymbols):
        """
            Modulate a vector of input symbols (numpy array format) using the chosen
             modem. The input symbols take integer values in the range 0 to M-1.
        """
        if isinstance(inputSymbols,list):
            inputSymbols = np.array(inputSymbols)
        
        if  not (0 <= inputSymbols.all() <= self.M-1):
            raise ValueError('Values for inputSymbols are beyond the range 0 to M-1')
        
        modulatedVec = self.constellation[inputSymbols]
        return modulatedVec #return modulated vector
    
    def demodulate(self,receivedSyms):
        """
            Demodulate a vector of received symbols using the chosen modem.            
        """        
        if isinstance(receivedSyms,list):
            receivedSyms = np.array(receivedSyms)
            
        detectedSyms= self.iqDetector(receivedSyms)
        return detectedSyms
    
    def iqDetector(self,receivedSyms):
        """
        Optimum Detector for 2-dim. signals (ex: MQAM,MPSK,MPAM) in IQ Plane
        Note: MPAM/BPSK are one dimensional modulations. The same function can be 
        applied for these modulations since quadrature is zero (Q=0)
        
        The function computes the pair-wise Euclidean distance of each point in the
        received vector against every point in the reference constellation. It then
        returns the symbols from the reference constellation that provide the
        minimum Euclidean distance.
        
        Parameters:
            receivedSyms : received symbol vector of complex form
        Returns:
            detectedSyms:decoded symbols that provide the minimum Euclidean distance        
        """
        from scipy.spatial.distance import cdist
        # received vector and reference in cartesian form
        XA = np.column_stack((np.real(receivedSyms),np.imag(receivedSyms))) 
        XB=np.column_stack((np.real(self.constellation),np.imag(self.constellation)))
        
        d = cdist(XA,XB,metric='euclidean') #compute pair-wise Euclidean distances
        detectedSyms = np.argmin(d,axis=1)#indices corresponding minimum Euclid. dist.
        return detectedSyms
    
