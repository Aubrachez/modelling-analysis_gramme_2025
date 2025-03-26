import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Longueur de la barre
L = 11  # Valeur par défaut de la longueur de la barre

# Création de la figure avec trois sous-graphiques
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(12, 5))

# Configuration du premier graphique (Mécanisme oscillant)
ax1.set_xlim(-5, 10)
ax1.set_ylim(-10, 20)
ax1.set_xticks(np.arange(-5, 11, 5))
ax1.set_yticks(np.arange(-10, 21, 5))
ax1.set_title("Mécanisme oscillant")
ax1.grid(True)

# Placer les objets sur le graphique
point, = ax1.plot([], [], 'ro', markersize=10)
line, = ax1.plot([], [], 'b-', lw=2)
bar, = ax1.plot([], [], 'g-', lw=2)
orange_ball, = ax1.plot([], [], 'yo', markersize=10)
vertical_line, = ax1.plot([], [], 'm-', lw=2)
purple_ball, = ax1.plot([], [], 'co', markersize=10)

# Configuration du deuxième graphique (Sinusoïde)
t = np.linspace(0, 2 * np.pi, 100)
y = np.sin(t)
ax2.set_ylim(-1.2, 1.2)
ax2.set_xlim(0, 2 * np.pi)
ax2.set_xlabel("Temps")
ax2.set_ylabel("Amplitude")
ax2.set_title("allongement RH")
line_sin, = ax2.plot(t, y, 'b')

# Configuration du troisième graphique (Sinusoïde)
t = np.linspace(0, 2 * np.pi, 100)
y = np.cos(t)
ax3.set_ylim(-1.2, 1.2)
ax3.set_xlim(0, 2 * np.pi)
ax3.set_xlabel("Temps")
ax3.set_ylabel("Amplitude")
ax3.set_title("allongement RV")
RV, = ax3.plot(t, y, 'b')

# Configuration du quatrième graphique (Sinusoïde)
t = np.linspace(0, 2 * np.pi, 100)
y = np.cos(t)
ax4.set_ylim(-1.2, 1.2)
ax4.set_xlim(0, 2 * np.pi)
ax4.set_xlabel("Temps")
ax4.set_ylabel("Amplitude")
ax4.set_title("vitesse masse")
masse, = ax4.plot(t, y, 'b')

# Configuration du cinquième graphique (Sinusoïde)
t = np.linspace(0, 2 * np.pi, 100)
y = np.cos(t)
ax5.set_ylim(-1.2, 1.2)
ax5.set_xlim(0, 2 * np.pi)
ax5.set_xlabel("Temps")
ax5.set_ylabel("Amplitude")
ax5.set_title("Angle theta")
theta, = ax5.plot(t, y, 'b')

# Fonction de mise à jour pour le mécanisme oscillant
def update_mechanism(i):
    x = 4 * np.cos(0.05 * i)
    y = 0
    point.set_data(x, y)
    line.set_data([x, 6], [y, y])
    fixed_x = 5
    distance_x = x - fixed_x
    if abs(distance_x) > L:
        distance_x = np.sign(distance_x) * L
    fixed_y = np.sqrt(L**2 - distance_x**2)
    bar.set_data([x, fixed_x], [y, fixed_y])
    orange_ball.set_data(fixed_x, fixed_y)
    vertical_length = 1 + 5 * ((fixed_y - min(0, fixed_y)) / L)
    vertical_line.set_data([fixed_x, fixed_x], [fixed_y, fixed_y - vertical_length])
    purple_ball.set_data(fixed_x, fixed_y - vertical_length)
    return [point, line, bar, orange_ball, vertical_line, purple_ball]

# Fonction de mise à jour pour la sinusoïde
def update_sin(frame):
    line_sin.set_ydata(np.sin(t + frame * 0.1))
    return line_sin,

def update_RV(frame):
    RV.set_ydata(np.cos(t + frame * 0.1))
    return RV,

def update_masse(frame):
    masse.set_ydata(-(np.cos(t + frame * 0.1)))
    return masse,

def update_theta(frame):
    theta.set_ydata(-(np.cos(t + frame * 0.1)))
    return theta,
# Création des animations
anim1 = FuncAnimation(fig, update_mechanism, frames=1000, interval=20, blit=True)
anim2 = FuncAnimation(fig, update_sin, frames=100, interval=50, blit=True)
anim3 = FuncAnimation(fig, update_RV, frames=100, interval=50, blit=True)
anim4 = FuncAnimation(fig, update_masse, frames=100, interval=50, blit=True)
anim5 = FuncAnimation(fig, update_theta, frames=100, interval=50, blit=True)
# Afficher le graphique
plt.show()
