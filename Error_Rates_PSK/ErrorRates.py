import numpy as np
from numpy import log2,sqrt,sin,pi,exp
from scipy.special import erfc
from scipy.integrate import quad

def ser_awgn(EbN0dBs,mod_type=None,M=0,coherence=None):
    """
    Theoretical Symbol Error Rates for various modulations over AWGN
    Parameters:
        EbN0dBs : list of SNR per bit values in dB scale
        mod_type : 'PSK','QAM','PAM','FSK'
        M : Modulation level for the chosen modulation.
            For PSK,PAM,FSK M can be any power of 2.
            For QAM M must be even power of 2 (square QAM only)
        coherence : 'coherent' for coherent FSK detection
                    'noncoherent' for noncoherent FSK detection
                This parameter is only applicable for FSK modulation
    Returns:
        SERs = list of symbol error rates
    """
    if mod_type==None:
        raise ValueError('Invalid value for mod_type')
    if (M<2) or ((M & (M -1))!=0): #if M not a power of 2
        raise ValueError('M should be a power of 2')
    
    func_dict = {'psk': psk_awgn,'qam':qam_awgn,'pam':pam_awgn,'fsk':fsk_awgn}
    
    gamma_s = log2(M)*(10**(EbN0dBs/10))
    if mod_type.lower()=='fsk': #call appropriate function
        return func_dict[mod_type.lower()](M,gamma_s,coherence) 
    else:
        return func_dict[mod_type.lower()](M,gamma_s) #call appropriate function

def psk_awgn(M,gamma_s):
    """
    Theoretical Symbol Error Rates for PSK over AWGN
    Parameters:
        M : Modulation level for the chosen modulation.
            For PSK, M can be any power of 2.
        gamma_s : list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    gamma_b = gamma_s/log2(M)
    if (M==2):
        SERs = 0.5*erfc(sqrt(gamma_b))
    elif M==4:
        Q = 0.5*erfc(sqrt(gamma_b))
        SERs = 2*Q-Q**2
    else:
        SERs = erfc(sqrt(gamma_s)*sin(pi/M))
    return SERs

def qam_awgn(M,gamma_s):
    """
    Theoretical Symbol Error Rates for square QAM over AWGN
    Parameters:
        M : Modulation level for the chosen modulation.
            For QAM, M must be even power of 2 (square QAM only).
        gamma_s : list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    if (M==1) or (np.mod(np.log2(M),2)!=0): # M not a even power of 2
        raise ValueError('Only square MQAM supported. M must be even power of 2')
    SERs = 1-(1-(1-1/sqrt(M))*erfc(sqrt(3/2*gamma_s/(M-1))))**2
    return SERs

def pam_awgn(M,gamma_s):
    """
    Theoretical Symbol Error Rates for PAM over AWGN
    Parameters:
        M : Modulation level for the chosen modulation.
            For PAM, M can be any power of 2.
        gamma_s : list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    SERs=2*(1-1/M)*0.5*erfc(sqrt(3*gamma_s/(M**2-1)))
    return SERs

def integrand(q,gamma_s,M):
    """
    Compute the integrand used for computing symbol error rates for coherent FSK        
    Parameters:
    q : represents the variable q in the above equation
    gamma_s : list of snr per symbol 
    M : Modulation level for the chosen modulation.
        For FSK, M can be any power of 2.
    Returns:
        The computed equation as a function
    """
    return (0.5*erfc((-q-np.sqrt(2*gamma_s))/np.sqrt(2)))**(M-1)\
        *1/np.sqrt(2*pi)*np.exp(-(q**2)/2)

def fsk_awgn(M_val,gamma_s_vals,coherence):
    """
    Theoretical Symbol Error Rates for FSK over AWGN
    Parameters:
        M_val : Modulation level for FSK modulation.
            For FSK, M can be any power of 2.
        gamma_s_vals: list of snr per symbol 
        coherence: 'coherent' for coherent FSK detection
                    'noncoherent' for noncoherent FSK detection
    Returns:
        SERs = list of symbol error rates
    """
    SERs = np.zeros(len(gamma_s_vals))
    if coherence.lower()=='coherent':
        for j,gamma_s in enumerate(gamma_s_vals):
            (y,_) =  quad(integrand,-np.inf,np.inf,(gamma_s,M_val))
            SERs[j] = 1- y
    elif coherence.lower()=='noncoherent':
        #use SymPy - symbolic mathematics for evaluating the SER equations
        from sympy import symbols,Symbol,Sum,exp,binomial,erfc,integrate,oo,sqrt
        M,i = symbols('M i', integer=True, positive=True)
        gamma = Symbol('gamma')
        s = Sum((-1)**(i+1)/(i+1)*binomial(M-1,i)*exp(-i/(i+1)*gamma),(i,1,M-1))
        for j,gamma_s in enumerate(gamma_s_vals):
            #evaluate the expression with values for M and gamma_s
            SERs[j] = s.evalf(subs={M:M_val,gamma:gamma_s})
    else:
        raise ValueError('For FSK coherence must be \'coherent\' or \'noncoherent\'')
    return SERs

def ser_rayleigh(EbN0dBs,mod_type=None,M=0):
    """
    Theoretical Symbol Error Rates for various modulations over noise added Rayleigh
    flat-fading channel
    Parameters:
        EbN0dBs : list of SNR per bit values in dB scale
        mod_type : 'PSK','QAM','PAM'
        M : Modulation level for the chosen modulation.
            For PSK,PAM M can be any power of 2.
            For QAM M must be even power of 2 (square QAM only)
    Returns:
        SERs = list of symbol error rates
    """
    if mod_type==None:
        raise ValueError('Invalid value for mod_type')
    if (M<2) or ((M & (M -1))!=0): #if M not a power of 2
        raise ValueError('M should be a power of 2')    
    func_dict = {'psk': psk_rayleigh,'qam':qam_rayleigh,'pam':pam_rayleigh}    
    gamma_s_vals = log2(M)*(10**(EbN0dBs/10))
    return func_dict[mod_type.lower()](M,gamma_s_vals) #call appropriate function

def mgf_rayleigh(g,gamma_s): 
    """
    Used to compute MGF function for Rayleigh flat-fading channel
    Parameters:
        g: represents the variable 'g' in the MGF equation 
        gamma_s : list of snr per symbol
    Returns:
        The MGF function
    """
    fun = lambda x: 1/(1+(g*gamma_s/(sin(x)**2))) # MGF function
    return fun        

def psk_rayleigh(M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for PSK over noise added Rayleigh
    flat-fading channel
    Parameters:
        M : Modulation level for the chosen modulation.
            For PSK, M can be any power of 2.
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    gamma_b = gamma_s_vals/log2(M)
    if (M==2):
        SERs = 0.5*(1-sqrt(gamma_b/(1+gamma_b)))
    else:
        SERs = np.zeros(len(gamma_s_vals))     
        g = (sin(pi/M))**2
        for i, gamma_s in enumerate(gamma_s_vals):
            (y,_) = quad(mgf_rayleigh(g,gamma_s),0,pi*(M-1)/M) #integration
            SERs[i] = (1/pi)*y
    return SERs

def qam_rayleigh(M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for square QAM over noise added Rayleigh
    flat-fading channel
    Parameters:
        M : Modulation level for the chosen modulation.
            For QAM, M must be an even power of 2 (square QAM only).
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    if (M==1) or (np.mod(np.log2(M),2)!=0): # M not a even power of 2
        raise ValueError('Only square MQAM supported. M must be even power of 2')    
    SERs = np.zeros(len(gamma_s_vals))
    g = 1.5/(M-1)
    for i, gamma_s in enumerate(gamma_s_vals):
        fun = mgf_rayleigh(g,gamma_s) # MGF function
        (y1,_) = quad(fun,0,pi/2) #integration 1
        (y2,_) = quad(fun,0,pi/4) #integration 2
        SERs[i] = 4/pi*(1-1/sqrt(M))*y1-4/pi*(1-1/sqrt(M))**2*y2
    return SERs

def pam_rayleigh(M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for PAM over noise added Rayleigh
    flat-fading channel
    Parameters:
        M : Modulation level for the chosen modulation.
            For PAM, M can be any power of 2.
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    SERs = np.zeros(len(gamma_s_vals))
    g = 3/(M**2-1)
    for i, gamma_s in enumerate(gamma_s_vals):
        (y1,_) = quad(mgf_rayleigh(g,gamma_s),0,pi/2) #integration 
        SERs[i] = 2*(M-1)/(M*pi)*y1
    return SERs

def ser_rician(K_dB,EbN0dBs,mod_type=None,M=0):
    """
    Theoretical Symbol Error Rates for various modulations over noise added Rician
    flat-fading channel
    Parameters:
        K_dB: Rician K-factor in dB    
        EbN0dBs : list of SNR per bit values in dB scale
        mod_type : 'PSK','QAM','PAM','FSK'
        M : Modulation level for the chosen modulation.
            For PSK,PAM M can be any power of 2.
            For QAM M must be even power of 2 (square QAM only)
    Returns:
        SERs = Symbol Error Rates
    """
    if mod_type==None:
        raise ValueError('Invalid value for mod_type')
    if (M<2) or ((M & (M -1))!=0): #if M not a power of 2
        raise ValueError('M should be a power of 2')
    
    func_dict = {'psk': psk_rician,'qam':qam_rician,'pam':pam_rician}
    gamma_s_vals = log2(M)*(10**(EbN0dBs/10))
    #call appropriate function
    return func_dict[mod_type.lower()](K_dB,M,gamma_s_vals)

def mgf_rician(K_dB,g,gamma_s): 
    """
    Used to compute MGF function for Rician flat-fading channel
    Parameters:
        K_dB: list of Rician K factors in dB
        g: represents the variable 'g' in the MGF equation 
        gamma_s : list of snr per symbol
    Returns:
        The MGF function
    """
    K = 10**(K_dB/10) # K factor in linear scale
    fun = lambda x: ((1+K)*sin(x)**2)/((1+K)*sin(x)**2+g*gamma_s)\
          *exp(-K*g*gamma_s/((1+K)*sin(x)**2+g*gamma_s)) # MGF function
    return fun #return the MGF function

def psk_rician(K_dB,M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for PSK over noise added Rician flat-fading channel
    Parameters:
        K_dB: list of Rician K factors in dB
        M : Modulation level for the chosen modulation.
            For PSK, M can be any power of 2.
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    gamma_b = gamma_s_vals/log2(M)
    
    if (M==2):
        SERs = 0.5*(1-sqrt(gamma_b/(1+gamma_b)))
    else:
        SERs = np.zeros(len(gamma_s_vals))     
        g = (sin(pi/M))**2
        for i, gamma_s in enumerate(gamma_s_vals):
            (y,_) = quad(mgf_rician(K_dB,g,gamma_s),0,pi*(M-1)/M) #integration
            SERs[i] = (1/pi)*y
    return SERs

def qam_rician(K_dB,M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for QAM over noise added Rician flat-fading channel
    Parameters:
        K_dB: list of Rician K factors in dB
        M : Modulation level for the chosen modulation.
            For QAM, M must be an even power of 2 (square QAM only).
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    if (M==1) or (np.mod(np.log2(M),2)!=0): # M not a even power of 2
        raise ValueError('Only square MQAM supported. M must be even power of 2')
    SERs = np.zeros(len(gamma_s_vals))
    g = 1.5/(M-1)
    for i, gamma_s in enumerate(gamma_s_vals):
        fun = mgf_rician(K_dB,g,gamma_s) #MGF function
        (y1,_) = quad(fun,0,pi/2) #integration 1
        (y2,_) = quad(fun,0,pi/4) #integration 2
        SERs[i] = 4/pi*(1-1/sqrt(M))*y1-4/pi*(1-1/sqrt(M))**2*y2
    return SERs

def pam_rician(K_dB,M,gamma_s_vals):
    """
    Theoretical Symbol Error Rates for PAM over noise added Rician flat-fading channel
    Parameters:
        K_dB: list of Rician K factors in dB
        M : Modulation level for the chosen modulation.
            For PAM, M can be any power of 2.
        gamma_s_vals: list of snr per symbol
    Returns:
        SERs = list of symbol error rates
    """
    SERs = np.zeros(len(gamma_s_vals))
    g = 3/(M**2-1)
    for i, gamma_s in enumerate(gamma_s_vals):
        (y1,_) = quad(mgf_rician(K_dB,g,gamma_s),0,pi/2) #integration 
        SERs[i] = 2*(M-1)/(M*pi)*y1
    return SERs