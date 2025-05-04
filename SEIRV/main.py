import matplotlib.pyplot as plt


# Population
P = 100
Et = [1.0]
It = [0.0]
Rt = [0.0]
V = 0
S0 = 100-Et[0]-V
St = [S0]

# Constants
beta = 0.4
gamma = 0.055
alpha = 0.142857

# Time
t = 0
dt = 0.01
T = [0.0]

for t in range(1600):
    St.append(St[-1] - beta * St[-1] * It[-1] * dt)
    Et.append(Et[-1] + beta * St[-1] * It[-1] * dt - alpha * Et[-1] * dt)
    It.append(It[-1] + (alpha * Et[-1] - gamma * It[-1]) * dt)
    Rt.append(Rt[-1] + gamma * It[-1] * dt)
    T.append(t/10)

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(T[:-1], St[:-1], label='Susceptibles')
plt.plot(T[:-1], Et[:-1], label='Exposats')
plt.plot(T[:-1], It[:-1], label='Infectats')
plt.plot(T[:-1], Rt[:-1], label='Recuperats')
plt.xlabel('Temps (dies)')
plt.ylabel('Nombre de persones')
plt.title('SEIR-V_95')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
