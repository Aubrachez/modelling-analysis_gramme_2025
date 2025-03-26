import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Longueur de la barre
L = 11

# Création de la figure avec cinq sous-graphiques
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(17, 5))

# --- Graphe 1 : Mécanisme oscillant ---
ax1.set_xlim(-5, 10)
ax1.set_ylim(-10, 20)
ax1.set_title("Mécanisme oscillant")
ax1.grid(True)
point, = ax1.plot([], [], 'ro', markersize=10)
line, = ax1.plot([], [], 'b-', lw=2)
bar, = ax1.plot([], [], 'g-', lw=2)
orange_ball, = ax1.plot([], [], 'yo', markersize=10)
vertical_line, = ax1.plot([], [], 'm-', lw=2)
purple_ball, = ax1.plot([], [], 'co', markersize=10)

# --- Graphe 2 : Allongement RH (longueur de la barre bleue) ---
ax2.set_ylim(0, 5)
ax2.set_xlim(0, 20)
ax2.set_title("Allongement RH")
ax2.set_xlabel("Temps")
ax2.set_ylabel("Longueur")
line_sin, = ax2.plot([], [], 'b')

# --- Graphe 3 : Allongement RV (longueur de la verticale) ---
ax3.set_ylim(0, 10)
ax3.set_xlim(0, 20)
ax3.set_title("Allongement RV")
ax3.set_xlabel("Temps")
ax3.set_ylabel("Longueur")
RV, = ax3.plot([], [], 'g')

# --- Graphe 4 : Vitesse masse (garde cos) ---
t = np.linspace(0, 2 * np.pi, 100)
y = np.cos(t)
ax4.set_ylim(-1.2, 1.2)
ax4.set_xlim(0, 2 * np.pi)
ax4.set_title("Vitesse masse")
ax4.set_xlabel("Temps")
ax4.set_ylabel("Amplitude")
masse, = ax4.plot(t, y, 'b')

# --- Graphe 5 : Angle theta (angle de la barre verte avec l’horizontale) ---
ax5.set_ylim(-np.pi/2, np.pi/2)
ax5.set_xlim(0, 20)
ax5.set_title("Angle θ (bar vs horizontal)")
ax5.set_xlabel("Temps")
ax5.set_ylabel("θ (radians)")
theta_plot, = ax5.plot([], [], 'm')

# Données à enregistrer
time_data = []
bar_lengths = []
vertical_lengths = []
theta_values = []

# Fonction de mise à jour du mécanisme
def update_mechanism(i):
    x = 4 * np.cos(0.05 * i)
    y = 0
    point.set_data(x, y)
    line.set_data([x, 6], [y, y])
    bar_length = abs(x - 6)
    bar_lengths.append(bar_length)

    # Mécanisme
    fixed_x = 5
    dx = x - fixed_x
    if abs(dx) > L:
        dx = np.sign(dx) * L
    dy = np.sqrt(L**2 - dx**2)
    bar.set_data([x, fixed_x], [y, dy])
    orange_ball.set_data(fixed_x, dy)

    # Calcul de l'angle de la barre
    theta = np.arctan2(dy, fixed_x - x)  # y/x
    theta_values.append(theta)

    # Vertical line
    vertical_length = 1 + 5 * ((dy - min(0, dy)) / L)
    vertical_line.set_data([fixed_x, fixed_x], [dy, dy - vertical_length])
    purple_ball.set_data(fixed_x, dy - vertical_length)
    vertical_lengths.append(vertical_length)

    # Temps
    time = 0.05 * i
    time_data.append(time)

    # Garde taille des listes
    max_len = 200
    for lst in [time_data, bar_lengths, vertical_lengths, theta_values]:
        if len(lst) > max_len:
            lst.pop(0)

    return [point, line, bar, orange_ball, vertical_line, purple_ball]

# Mise à jour des courbes dynamiques
def update_sin(frame):
    if len(time_data) < 2:
        return line_sin,
    line_sin.set_data(time_data, bar_lengths)
    ax2.set_xlim(max(0, time_data[-1] - 10), time_data[-1] + 1)
    ax2.set_ylim(0, max(bar_lengths[-50:]) + 1)
    return line_sin,

def update_RV(frame):
    if len(time_data) < 2:
        return RV,
    RV.set_data(time_data, vertical_lengths)
    ax3.set_xlim(max(0, time_data[-1] - 10), time_data[-1] + 1)
    ax3.set_ylim(0, max(vertical_lengths[-50:]) + 1)
    return RV,

def update_theta(frame):
    if len(time_data) < 2:
        return theta_plot,
    theta_plot.set_data(time_data, theta_values)
    ax5.set_xlim(max(0, time_data[-1] - 10), time_data[-1] + 1)
    ax5.set_ylim(-np.pi/2, np.pi/2)
    return theta_plot,

# Graphe masse (inchangé)
def update_masse(frame):
    masse.set_ydata(-(np.cos(t + frame * 0.1)))
    return masse,

# Animations
anim1 = FuncAnimation(fig, update_mechanism, frames=1000, interval=20, blit=True)
anim2 = FuncAnimation(fig, update_sin, frames=1000, interval=20, blit=True)
anim3 = FuncAnimation(fig, update_RV, frames=1000, interval=20, blit=True)
anim4 = FuncAnimation(fig, update_masse, frames=100, interval=50, blit=True)
anim5 = FuncAnimation(fig, update_theta, frames=1000, interval=20, blit=True)

# Affichage
plt.tight_layout()
plt.show()
