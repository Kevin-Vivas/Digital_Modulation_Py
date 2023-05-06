import numpy as np
import matplotlib.pyplot as plt

# Primera figura
x1 = -2
x2 = 2
y1 = 2
y2 = -2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10)) # Crea una figura con dos subtramas
plt.subplots_adjust(wspace=0.5) # Ajusta el espacio entre las subtramas

ax1.axis([x1,x2,y2,y1])
ax1.axis('on')
ax1.grid(False)
ax1.set_title('Diagrama-Fasorial-8PSK')


# Grid
dx=0.2
dy=-0.2
for x in np.arange(x1,x2,dx):
    for y in np.arange(y1,y2,dy):
        ax1.scatter(x,y,s=0,color='lightgray')

ax1.arrow(0,0,1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax1.text(-0.305,1.700,'Cos(wct)',color='k')
ax1.arrow(0,0,-1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax1.text(-0.305,-1.700,'-Cos(wct)',color='k')

ax1.arrow(0,0,0,1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax1.text(1,0.1,'Sen(wct)',color='k')
ax1.arrow(0,0,0,-1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax1.text(-1.500,0.1,'-Sen(wct)',color='k')
# Ejes de coordenadas
ax1.arrow(0,0,-0.541,-1.307,head_length=0.1,head_width=0.1,color='blue')
ax1.text(-0.700,-1.580,'(000)',color='red')

ax1.arrow(0,0,-1.307,-0.541,head_length=0.1,head_width=0.1,color='blue')
ax1.text(-1.700,-0.600,'(001)',color='red')

ax1.arrow(0,0,0.541,-1.307,head_length=0.1,head_width=0.1,color='blue')
ax1.text(0.430,-1.500,'(010)',color='red')

ax1.arrow(0,0,1.307,-0.541,head_length=0.1,head_width=0.1,color='blue')
ax1.text(1.500,-0.600,'(011)',color='red')

ax1.arrow(0,0,-0.541,1.307,head_length=0.1,head_width=0.1,color='blue')
ax1.text(-0.700,1.490,'(100)',color='red')

ax1.arrow(0,0,-1.307,0.541,head_length=0.1,head_width=0.1,color='blue')
ax1.text(-1.700,0.600,'(101)',color='red')


ax1.arrow(0,0,0.541,1.307,head_length=0.1,head_width=0.1,color='blue')
ax1.text(0.500,1.500,'(110)',color='red')

ax1.arrow(0,0,1.307,0.541,head_length=0.1,head_width=0.1,color='blue')
ax1.text(1.500,0.600,'(111)',color='red')

# Segunda figura
#t = np.linspace(-np.pi, np.pi, 1000)
#y = np.sin(t)

#ax2.plot(t, y)

ax2.axis([x1,x2,y2,y1])
ax2.axis('on')
ax2.grid(False)
ax2.set_title('Diagrama-de-Constelación-8PSK')
#Cordenadas 
ax2.arrow(0,0,1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax2.text(-0.305,1.700,'Cos(wct)',color='k')
ax2.arrow(0,0,-1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax2.text(-0.305,-1.700,'-Cos(wct)',color='k')
ax2.arrow(0,0,0,1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax2.text(1,0.1,'Sen(wct)',color='k')
ax2.arrow(0,0,0,-1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax2.text(-1.500,0.1,'-Sen(wct)',color='k')

#Caso(000)
ax2.scatter(-0.541,-1.307,s=100, color='blue')
ax2.text(-0.700,-1.580,'(000)',color='red')
#Caso(001)
ax2.scatter(-1.307,-0.541,s=100, color='blue')
ax2.text(-1.700,-0.600,'(001)',color='red')

#Caso(010)
ax2.scatter(0.541,-1.307,s=100, color='blue')
ax2.text(0.430,-1.500,'(010)',color='red')

#Caso(011)
ax2.scatter(1.307,-0.541,s=100, color='blue')
ax2.text(1.500,-0.600,'(011)',color='red')

#Caso(100)
ax2.scatter(-0.541,1.307,s=100, color='blue')
ax2.text(-0.700,1.490,'(100)',color='red')

#Caso(101)
ax2.scatter(-1.307,0.541,s=100, color='blue')
ax2.text(-1.700,0.600,'(101)',color='red')

#Caso(110)
ax2.scatter(0.541,1.307,s=100, color='blue')
ax2.text(0.500,1.500,'(110)',color='red')

#Caso(111)
ax2.scatter(1.307,0.541,s=100, color='blue')
ax2.text(1.500,0.600,'(111)',color='red')

plt.show()
