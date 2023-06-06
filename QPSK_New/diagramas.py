from scipy.spatial import distance
import matplotlib.pyplot as plt

# Símbolos a graficar en el diagrama de constelación
symbols = [1+1j, -1+1j, 1-1j, -1-1j]

# Coordenadas a las que apuntarán las flechas
coordinates = [(-1,1), (1,1), (-1,-1), (1,-1)]

# Crear la figura y los dos objetos Axes
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Graficar las flechas en el primer objeto Axes
for i in range(len(symbols)):
    # Encontrar la coordenada más cercana en la lista de coordenadas
    closest_coord = min(coordinates, key=lambda x: distance.euclidean(x, (symbols[i].real, symbols[i].imag)))
    # Obtener el índice de la coordenada más cercana
    idx = coordinates.index(closest_coord)
    # Graficar la flecha
    ax1.arrow(0, 0, symbols[i].real, symbols[i].imag, head_width=0.1, head_length=0.1, fc='blue', ec='blue')

# Graficar los puntos en el segundo objeto Axes
ax2.scatter([coord[0] for coord in coordinates], [coord[1] for coord in coordinates], color='blue')

# Configurar los límites de los ejes para ambos objetos Axes
ax1.set_xlim(-2,2)
ax1.set_ylim(-2,2)
ax2.set_xlim(-2,2)
ax2.set_ylim(-2,2)

# Agregar títulos y etiquetas a los objetos Axes
ax1.set_title("Diagrama Fasorial")
ax1.set_xlabel("Eje real")
ax1.set_ylabel("Eje imaginario")

ax2.set_title("Diagrama de constelación")
ax2.set_xlabel("Eje real")
ax2.set_ylabel("Eje imaginario")

ax1.arrow(0,0,1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax1.text(-0.305,1.700,'Cos(wct)',color='k')
ax1.arrow(0,0,-1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax1.text(-0.305,-1.700,'-Cos(wct)',color='k')

ax1.arrow(0,0,0,1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax1.text(1,0.1,'Sen(wct)',color='k')
ax1.arrow(0,0,0,-1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax1.text(-1.500,0.1,'-Sen(wct)',color='k')
ax1.text(-1.2,1.2,'(10)',color='red')
ax1.text(1,1.2,'(11)',color='red')
ax1.text(-1.40,-1.4,'(00)',color='red')
ax1.text(1.113,-1.150,'(01)',color='red')




ax2.arrow(0,0,1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax2.text(-0.305,1.700,'Cos(wct)',color='k')
ax2.arrow(0,0,-1.5,0,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08) 
ax2.text(-0.305,-1.700,'-Cos(wct)',color='k')

ax2.arrow(0,0,0,1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax2.text(1,0.1,'Sen(wct)',color='k')
ax2.arrow(0,0,0,-1.5,linewidth=1,color='k',linestyle='-',head_length=0.1,head_width=0.08)
ax2.text(-1.500,0.1,'-Sen(wct)',color='k')
ax2.text(0.930,-1.225,'(01)',color='red')
ax2.text(-1.127,-1.225,'(00)',color='red')
ax2.text(-1.2,1.2,'(10)',color='red')
ax2.text(0.9,1.2,'(11)',color='red')

# Mostrar la figura
plt.show()
