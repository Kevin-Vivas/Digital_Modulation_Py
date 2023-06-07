import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn

def qpsk_mod(a, fc, OF, enable_plot = False):
    """
    Modulate an incoming binary stream using conventional QPSK
    Parameters:
        a : input binary data stream (0's and 1's) to modulate
        fc : carrier frequency in Hertz
        OF : oversampling factor - at least 4 is better
        enable_plot : True = plot transmitter waveforms (default False)
    Returns:
        result : Dictionary containing the following keyword entries:
          s(t) : QPSK modulated signal vector with carrier i.e, s(t)
          I(t) : baseband I channel waveform (no carrier)
          Q(t) : baseband Q channel waveform (no carrier)
          t : time base for the carrier modulated signal
    """
    L = 2*OF # samples in each symbol (QPSK has 2 bits in each symbol)
    I = a[0::2];Q = a[1::2] #even and odd bit streams
    # even/odd streams at 1/2Tb baud
        
    from scipy.signal import upfirdn #NRZ encoder
    I = upfirdn(h=[1]*L, x=2*I-1, up = L)
    Q = upfirdn(h=[1]*L, x=2*Q-1, up = L)
    
    fs = OF*fc # sampling frequency 
    t=np.arange(0,len(I)/fs,1/fs)  #time base    
    
    I_t = I*np.cos(2*np.pi*fc*t);Q_t = -Q*np.sin(2*np.pi*fc*t)
    s_t = I_t + Q_t # QPSK modulated baseband signal
    
    if enable_plot:
        fig = plt.figure(constrained_layout=True)        
    
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 0])
        ax4 = fig.add_subplot(gs[1, 1])
        ax5 = fig.add_subplot(gs[-1,:])  
              
        # show first few symbols of I(t), Q(t)
        ax1.plot(t,I)       
        ax2.plot(t,Q)
        ax3.plot(t,I_t,'r')
        ax4.plot(t,Q_t,'r')
        
        ax1.set_title('I(t)')
        ax2.set_title('Q(t)')
        ax3.set_title('$I(t) cos(2 \pi f_c t)$')
        ax4.set_title('$Q(t) sin(2 \pi f_c t)$')
        
        ax1.set_xlim(0,20*L/fs);ax2.set_xlim(0,20*L/fs)
        ax3.set_xlim(0,20*L/fs);ax4.set_xlim(0,20*L/fs)
        ax5.plot(t,s_t);ax5.set_xlim(0,20*L/fs);fig.show()
        ax5.set_title('$s(t) = I(t) cos(2 \pi f_c t) - Q(t) sin(2 \pi f_c t)$')
    
    result = dict()
    result['s(t)'] =s_t;result['I(t)'] = I;result['Q(t)'] = Q;result['t'] = t           
    return result

def oqpsk_mod(a,fc,OF,enable_plot=False):
    """
    Modulate an incoming binary stream using OQPSK
    Parameters:
        a : input binary data stream (0's and 1's) to modulate
        fc : carrier frequency in Hertz
        OF : oversampling factor - at least 4 is better
        enable_plot : True = plot transmitter waveforms (default False)
    Returns:
        result : Dictionary containing the following keyword entries:
          s(t) : QPSK modulated signal vector with carrier i.e, s(t)
          I(t) : baseband I channel waveform (no carrier)
          Q(t) : baseband Q channel waveform (no carrier)
          t : time base for the carrier modulated signal
    """
    L = 2*OF # samples in each symbol (QPSK has 2 bits in each symbol)
    I = a[0::2];Q = a[1::2] #even and odd bit streams
    # even/odd streams at 1/2Tb baud
     #NRZ encoder
    I = upfirdn(h=[1]*L, x=2*I-1, up = L)
    Q = upfirdn(h=[1]*L, x=2*Q-1, up = L)

    I = np.hstack((I,np.zeros(L//2))) # padding at end
    Q = np.hstack((np.zeros(L//2),Q)) # padding at start
    
    fs = OF*fc # sampling frequency 
    t=np.arange(0,len(I)/fs,1/fs)  #time base
    I_t = I*np.cos(2*np.pi*fc*t);Q_t = -Q*np.sin(2*np.pi*fc*t)
    s = I_t + Q_t # QPSK modulated baseband signal
    
    if enable_plot:
        fig = plt.figure(constrained_layout=True)
        
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0]);ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 0]);ax4 = fig.add_subplot(gs[1, 1])
        ax5 = fig.add_subplot(gs[-1,:])
        
        # show first few symbols of I(t), Q(t)
        ax1.plot(t,I);ax1.set_title('I(t)')        
        ax2.plot(t,Q);ax2.set_title('Q(t)')
        ax3.plot(t,I_t,'r');ax3.set_title('$I(t) cos(2 \pi f_c t)$')
        ax4.plot(t,Q_t,'r');ax4.set_title('$Q(t) sin(2 \pi f_c t)$')
        ax1.set_xlim(0,20*L/fs);ax2.set_xlim(0,20*L/fs)
        ax3.set_xlim(0,20*L/fs);ax4.set_xlim(0,20*L/fs)
        ax5.plot(t,s);ax5.set_xlim(0,20*L/fs);fig.show()
        ax5.set_title('$s(t) = I(t) cos(2 \pi f_c t) - Q(t) sin(2 \pi f_c t)$')
        
        fig, axs = plt.subplots(1, 1)
        axs.plot(I,Q);fig.show()#constellation plot
    result = dict()
    result['s(t)'] =s;result['I(t)'] = I;result['Q(t)'] = Q;result['t'] = t           
    return result

def piBy4_dqpsk_mod(a,fc,OF,enable_plot = False):
    """
    Modulate a binary stream using pi/4 DQPSK
    Parameters:
        a : input binary data stream (0's and 1's) to modulate
        fc : carrier frequency in Hertz
        OF : oversampling factor
    Returns:
        result : Dictionary containing the following keyword entries:
          s(t) : pi/4 QPSK modulated signal vector with carrier
          U(t) : differentially coded I-channel waveform (no carrier)
          V(t) : differentially coded Q-channel waveform (no carrier)
          t: time base
    """
    (u,v)= piBy4_dqpsk_diff_encoding(a) # Differential Encoding for pi/4 QPSK
    #Waveform formation (similar to conventional QPSK)
    L = 2*OF # number of samples in each symbol (QPSK has 2 bits/symbol)    
    U = np.tile(u, (L,1)).flatten('F')# odd bit stream at 1/2Tb baud
    V = np.tile(v, (L,1)).flatten('F')# even bit stream at 1/2Tb baud
    
    fs = OF*fc # sampling frequency    
    t=np.arange(0, len(U)/fs,1/fs) #time base
    U_t = U*np.cos(2*np.pi*fc*t)
    V_t = -V*np.sin(2*np.pi*fc*t)
    s_t = U_t + V_t
    
    if enable_plot:
        fig = plt.figure(constrained_layout=True)
        
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0]);ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, 0]);ax4 = fig.add_subplot(gs[1, 1])
        ax5 = fig.add_subplot(gs[-1,:])        
        ax1.plot(t,U);ax2.plot(t,V)
        ax3.plot(t,U_t,'r');ax4.plot(t,V_t,'r')
        ax5.plot(t,s_t) #QPSK waveform zoomed to first few symbols        
        ax1.set_ylabel('U(t)-baseband');ax2.set_ylabel('V(t)-baseband')
        ax3.set_ylabel('U(t)-with carrier');ax4.set_ylabel('V(t)-with carrier')
        ax5.set_ylabel('s(t)');ax5.set_xlim([0,10*L/fs])
        ax1.set_xlim([0,10*L/fs]);ax2.set_xlim([0,10*L/fs])
        ax3.set_xlim([0,10*L/fs]);ax4.set_xlim([0,10*L/fs])
        fig.show()
        
    result = dict()
    result['s(t)'] =s_t;result['U(t)'] = U;result['V(t)'] = V;result['t'] = t
    return result

def msk_mod(a, fc, OF, enable_plot = False):
    """
    Modulate an incoming binary stream using MSK
    Parameters:
        a : input binary data stream (0's and 1's) to modulate
        fc : carrier frequency in Hertz
        OF : oversampling factor (at least 4 is better)
    Returns:
        result : Dictionary containing the following keyword entries:
          s(t) : MSK modulated signal with carrier
          sI(t) : baseband I channel waveform(no carrier)
          sQ(t) : baseband Q channel waveform(no carrier)
          t: time base
    """ 
    ak = 2*a-1 # NRZ encoding 0-> -1, 1->+1
    ai = ak[0::2]; aq = ak[1::2] # split even and odd bit streams
    L = 2*OF # represents one symbol duration Tsym=2xTb
    
    #upsample by L the bits streams in I and Q arms
    from scipy.signal import upfirdn, lfilter
    ai = upfirdn(h=[1], x=ai, up = L)
    aq = upfirdn(h=[1], x=aq, up = L)
    
    aq = np.pad(aq, (L//2,0), 'constant') # delay aq by Tb (delay by L/2)
    ai = np.pad(ai, (0,L//2), 'constant') # padding at end to equal length of Q
    
    #construct Low-pass filter and filter the I/Q samples through it
    Fs = OF*fc;Ts = 1/Fs;Tb = OF*Ts
    t = np.arange(0,2*Tb+Ts,Ts)
    h = np.sin(np.pi*t/(2*Tb))# LPF filter
    sI_t = lfilter(b = h, a = [1], x = ai) # baseband I-channel
    sQ_t = lfilter(b = h, a = [1], x = aq) # baseband Q-channel
    
    t=np.arange(0, Ts*len(sI_t), Ts) # for RF carrier
    sIc_t = sI_t*np.cos(2*np.pi*fc*t) #with carrier
    sQc_t = sQ_t*np.sin(2*np.pi*fc*t) #with carrier
    s_t =  sIc_t - sQc_t# Bandpass MSK modulated signal
    
    if enable_plot:
        fig, (ax1,ax2,ax3) = plt.subplots(3, 1)
        
        ax1.plot(t,sI_t);ax1.plot(t,sIc_t,'r')
        ax2.plot(t,sQ_t);ax2.plot(t,sQc_t,'r')
        ax3.plot(t,s_t,'--')        
        ax1.set_ylabel('$s_I(t)$');ax2.set_ylabel('$s_Q(t)$')
        ax3.set_ylabel('s(t)')        
        ax1.set_xlim([-Tb,20*Tb]);ax2.set_xlim([-Tb,20*Tb])
        ax3.set_xlim([-Tb,20*Tb])
        fig.show()
        
    result = dict()
    result['s(t)']=s_t;result['sI(t)']=sI_t;result['sQ(t)']=sQ_t;result['t']=t
    return result

def piBy4_dqpsk_diff_encoding(a,enable_plot=False):
    """
    Phase Mapper for pi/4-DQPSK modulation
    Parameters:
        a : input stream of binary bits
    Returns:
        (u,v): tuple, where
           u : differentially coded I-channel bits
           v : differentially coded Q-channel bits    
    """
    from numpy import pi, cos, sin
    if len(a)%2: raise ValueError('Length of binary stream must be even')
    I = a[0::2] # odd bit stream
    Q = a[1::2] # even bit stream
    # club 2-bits to form a symbol and use it as index for dTheta table
    m = 2*I+Q
    dTheta = np.array([-3*pi/4, 3*pi/4, -pi/4, pi/4]) #LUT for pi/4-DQPSK
    u = np.zeros(len(m)+1);v = np.zeros(len(m)+1)
    u[0]=1; v[0]=0 # initial conditions for uk and vk
    for k in range(0,len(m)):
        u[k+1] = u[k] * cos(dTheta[m[k]]) - v[k] * sin(dTheta[m[k]])
        v[k+1] = u[k] * sin(dTheta[m[k]]) + v[k] * cos(dTheta[m[k]])
    if enable_plot:#constellation plot
        fig, axs = plt.subplots(1, 1)
        axs.plot(u,v,'o');
        axs.set_title('Constellation');fig.show()
    return (u,v)