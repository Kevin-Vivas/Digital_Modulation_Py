from sympy.combinatorics.graycode import GrayCode
from numpy.matlib import repmat
import numpy as np
from commpy.modulation import QAMModem
import matplotlib.pyplot as plt

def GrayMapping(M):
    L = int(np.sqrt(M) - 1)
    bitsSymb = int(np.log2(M))

    PAM = np.arange(-L, L + 1, 2)
    PAM = np.array([PAM])

    # generate complex square-QAM constellation
    const = repmat(PAM, L + 1, 1) + 1j * repmat(np.flip(PAM.T, 0), 1, L + 1)
    const = const.T

    for ind in np.arange(1, L + 1, 2):
        const[ind] = np.flip(const[ind], 0)

    code = GrayCode(bitsSymb)
    a = list(code.generate_gray())

    const_ = np.zeros((M, 2), dtype=complex)
    const = const.reshape(M, 1)

    for ind in range(0, M):
        const_[ind, 0] = const[ind, 0]  # complex constellation symbol
        const_[ind, 1] = int(a[ind], 2)  # mapped bit sequence (as integer decimal)

    # sort complex symbols column according to their mapped bit sequence (as integer decimal)
    const = const_[const_[:, 1].real.argsort()]

    return const

# Generate QAM16 constellation points
QAM16 = QAMModem(16)
QAM16.constellation = GrayMapping(16)[:, 0] # cambia M-QAM

# Create figure and two subplots for constellation and phasor diagrams
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

# Plot constellation diagram on first subplot
ax1.scatter(QAM16.constellation.real, QAM16.constellation.imag, color='blue')
ax1.set_xlim([-5, 5])
ax1.set_ylim([-5, 5])
ax1.grid(False)
ax1.set_title('QAM16 Constellation')
ax1.axhline(0, color='k', linestyle='--', linewidth=2)
ax1.axvline(0, color='k', linestyle='--',linewidth=2)

# plot QAM16 phasor diagram
angles = np.angle(QAM16.constellation, deg=True)
magnitudes = np.abs(QAM16.constellation)
for i in range(len(QAM16.constellation)):
    ax2.quiver(0, 0, QAM16.constellation[i].real, QAM16.constellation[i].imag, angles='xy', scale_units='xy', scale=1, color='blue')
    ax2.set_xlim([-4, 4])
    ax2.set_ylim([-4, 4])
    ax2.grid(False)
    ax2.set_title('QAM16 Phasor Diagram')
    ax2.axhline(0, color='k', linestyle='--', linewidth=2)
    ax2.axvline(0, color='k', linestyle='--',linewidth=2)

# Display the figure
plt.show()





   



