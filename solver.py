import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- PARAMÈTRES NON-DIMENSIONNELS ---
alpha = 2     # Constante ressort vertical (k1 L / mg)
beta = 9       # Constante ressort horizontal (k2 L / mg)
gamma = 2      # Rapport des masses M/m
lambda1 = 1    # Longueur mini ressort vertical
lambda2 = 1    # Longueur mini ressort horizontal
damping = 0.0 # Dissipation

# --- ÉQUATIONS DIFFÉRENTIELLES ---
def ode_system(tau, y):
    theta, theta_dot, mu, mu_dot = y

    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    # Longueurs effectives
    L_vert = sin_theta - mu
    L_horiz = cos_theta

    # Forces des ressorts avec limites (valeurs planchers)
    L_vert_eff = max(L_vert, lambda1)
    L_horiz_eff = max(L_horiz, lambda2)

    f_spring_vert = alpha * (L_vert_eff - lambda1)
    f_spring_horiz = beta * (L_horiz_eff - lambda2)

    # Moments
    inertia = 4 / 3  # 1 + (1/3)

    torque_gravity = -np.sin(theta)
    torque_damping = -damping * theta_dot
    torque_spring_vert = -f_spring_vert * cos_theta
    torque_spring_horiz = -f_spring_horiz * sin_theta

    theta_ddot = (torque_gravity + torque_spring_vert + torque_spring_horiz + torque_damping) / inertia
    mu_ddot = gamma * f_spring_vert - 1

    return [theta_dot, theta_ddot, mu_dot, mu_ddot]

# --- CONDITIONS INITIALES ---
theta0 = 0.0  # angle vertical
mu0 = 0.0     # masse au niveau de la roue (mu = 0)
theta_dot0 = 0.0

mu_dot0 = 0.0
y0 = [theta0, theta_dot0, mu0, mu_dot0]

# --- INTÉGRATION NUMÉRIQUE ---
T_max = 500
t_eval = np.linspace(0, T_max, 2000)
sol = solve_ivp(ode_system, [0, T_max], y0, t_eval=t_eval, method='RK45', rtol=1e-8)

# --- EXTRACTION DES SOLUTIONS ---
tau = sol.t
theta = sol.y[0]
print(sol.y[0])
theta_dot = sol.y[1]
mu = sol.y[2]
mu_dot = sol.y[3]

# --- ÉNERGIE TOTALE ---
def energy(theta, theta_dot, mu, mu_dot):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    
    # Longueurs des ressorts avec minimums
    L_vert = np.maximum(sin_theta - mu, lambda1)
    L_horiz = np.maximum(cos_theta, lambda2)

    kinetic = 0.5 * (4/3) * theta_dot**2 + 0.5 * gamma * mu_dot**2
    potential = -np.cos(theta) \
                + 0.5 * alpha * (L_vert - lambda1)**2 \
                + 0.5 * beta * (L_horiz - lambda2)**2 \
                + gamma * mu
    return kinetic + potential

E = energy(theta, theta_dot, mu, mu_dot)

# --- AFFICHAGE DES RÉSULTATS ---
plt.figure(figsize=(14, 8))

plt.subplot(3, 2, 1)
plt.plot(tau, theta, label='θ(t)')
plt.plot(tau, mu, label='μ(t)')
plt.xlabel("τ (temps sans dimension)")
plt.ylabel("États du système")
plt.title("Évolution de θ(t) et μ(t)")
plt.legend()
plt.grid()

plt.subplot(3, 2, 2)
plt.plot(tau, E - E[0], label='ΔE = E(t) - E(0)')
plt.xlabel("τ")
plt.ylabel("Variation d'énergie")
plt.title("Conservation de l'énergie")
plt.grid()
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(tau, theta_dot, label="θ̇(t)", color='tab:orange')
plt.xlabel("τ")
plt.ylabel("Vitesse angulaire")
plt.title("Vitesse θ̇(t)")
plt.legend()
plt.grid()

plt.subplot(3, 2, 4)
plt.plot(tau, mu_dot, label="μ̇(t)", color='tab:green')
plt.xlabel("τ")
plt.ylabel("Vitesse μ̇(t)")
plt.title("Vitesse verticale μ̇(t)")
plt.legend()
plt.grid()
height_mass = np.sin(theta) - mu

plt.subplot(3, 2, 5)
plt.plot(tau, height_mass, label="Hauteur de la masse m", color='tab:red')
plt.xlabel("τ")
plt.ylabel("Hauteur (sans dimension)")
plt.title("Hauteur de la masse suspendue par rapport au sol")
plt.grid()
plt.legend()

# --- ALLONGEMENT DU RESSORT HORIZONTAL ---
elong_horiz = -(np.cos(theta) - lambda2)

plt.subplot(3, 2, 6)
plt.plot(tau, elong_horiz, label="Allongement ressort horizontal", color='tab:purple')
plt.xlabel("τ")
plt.ylabel("Allongement (sans dimension)")
plt.title("Allongement du ressort horizontal")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()




