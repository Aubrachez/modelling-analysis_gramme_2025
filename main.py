import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Longueur de la barre
L = 11  # Valeur par défaut de la longueur de la barre

# Initialiser la figure
fig, ax = plt.subplots()
ax.set_xlim(-5, 10)  # Limites de l'axe X
ax.set_ylim(-10, 20)  # Limites de l'axe Y

# Définir l'échelle avec un intervalle de 5 unités par case
ax.set_xticks(np.arange(-5, 11, 5))  # Échelle de 5 en horizontal
ax.set_yticks(np.arange(-10, 21, 5))  # Échelle de 5 en vertical

# Placer les objets sur le graphique
point, = ax.plot([], [], 'ro', markersize=10)  # point rouge
line, = ax.plot([], [], 'b-', lw=2)  # ligne bleue
bar, = ax.plot([], [], 'g-', lw=2)  # barre verte
orange_ball, = ax.plot([], [], 'yo', markersize=10)  # bille orange
vertical_line, = ax.plot([], [], 'm-', lw=2)  # ligne verticale magenta
purple_ball, = ax.plot([], [], 'co', markersize=10)  # bille cyan

# Fonction de mise à jour
def update(i):
    # Faire osciller la bille de x = 4 à x = 0 (mouvement décroissant)
    x = 4 * np.cos(0.05 * i)  # Oscillation entre 4 et 0 (en utilisant le cosinus)
    y = 0
    point.set_data(x, y)
    
    # Mise à jour de la ligne
    line.set_data([x, 6], [y, y])  # Relier le point à x=6

    # Position de l'extrémité de la barre qui est fixée à x=5
    fixed_x = 5
    distance_x = x - fixed_x

    # Si la distance est plus grande que la longueur de la barre, ajuster pour éviter des valeurs non réalistes
    if abs(distance_x) > L:
        distance_x = np.sign(distance_x) * L

    # Calcul de la position verticale de l'extrémité fixe de la barre, en maintenant la longueur constante
    fixed_y = np.sqrt(L**2 - distance_x**2)  # Calculer la position verticale de l'extrémité fixe de la barre

    # Relier le point à l'extrémité fixe de la barre
    bar.set_data([x, fixed_x], [y, fixed_y])  
    
    # Mettre la bille orange à l'extrémité mobile de la barre verte
    orange_ball.set_data(fixed_x, fixed_y)
    
    # Calculer la longueur de la ligne verticale oscillante
    vertical_length = 1 + 5 * ((fixed_y - min(0, fixed_y)) / L)  # Oscillation entre 1 et 5
    vertical_line.set_data([fixed_x, fixed_x], [fixed_y, fixed_y - vertical_length])
    
    # Mettre la bille cyan à l'extrémité inférieure de la ligne verticale
    purple_ball.set_data(fixed_x, fixed_y - vertical_length)
    
    return [point, line, bar, orange_ball, vertical_line, purple_ball]

# Animation
anim = FuncAnimation(fig, update, frames=1000, interval=20, blit=True)

# Afficher le graphique
plt.title(f"Projet de modelling & analysis with a mass of {L} and a spring constant of 1")
plt.grid(True)
plt.show()
