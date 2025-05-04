# Vaccination Model: Vaccine not effective + Immunity Simulation + Age Simulation

import matplotlib.pyplot as plt
import numpy as np
import random as random
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection


def stop_animation():
    global inf_list, sus_list, exp_list, vac_list, rec_list, xy, inf, inf_timer, \
        susceptible, exposed, infected, recovered, vaccinated, data_counter
    # Stop animation
    ani.event_source.stop()
    print("Animation restarted.")
    data_counter += 1
    print(data_counter)
    # Print info to SIM0.txt
    with open("Vac_95.txt", "a") as f:
        print("Susceptible: ", file=f)
        print(sus_list, file=f)
        print("Exposed: ", file=f)
        print(exp_list, file=f)
        print("Infected: ", file=f)
        print(inf_list, file=f)
        print("Recovered: ", file=f)
        print(rec_list, file=f)
        print("Vaccinated: ", file=f)
        print(vac_list, file=f)
        print("\n ", file=f)
    # Clear list of encounters
    sus_list = []
    exp_list = []
    inf_list = []
    rec_list = []
    vac_list = []
    susceptible = sus_ini
    exposed = exp_ini
    infected = inf_ini
    recovered = rec_ini
    vaccinated = vac_ini
    # New positions
    xy = [[random.randint(0, N - 1), random.randint(0, N - 1)] for _ in range(M)]
    # Create Population
    inf = [0 if z < vac_ini else 1 for z in range(M)]
    infected_starer = random.randint(vac_ini, M)
    inf[infected_starer] = 2
    inf_timer = {infected_starer: 0}
    # Restart Animation
    ani.event_source.start()


def time():
    global susceptible, exposed, infected, recovered, vaccinated, timer
    timer += 1
    red_circles = []
    green_circles = []
    yellow_circles = []
    for o in range(M):
        # Position Changes
        x_new = xy[o][0] + random.randint(-1, 1)
        y_new = xy[o][1] + random.randint(-1, 1)
        xy[o][0] = max(0, min(N - 1, x_new))
        xy[o][1] = max(0, min(N - 1, y_new))
        grid[xy[o][0], xy[o][1]] += 1  # Increment value at position
        # Red circle for infected individuals
        if inf[o] == 2:
            inf_timer[o] += 1
            if inf_timer[o] > inc_period:
                if inf_timer[o] == inc_period + 1:
                    infected += 1
                    exposed -= 1
                red_circles.append(Circle((xy[o][1], xy[o][0]), 0.4, fill=False))
                for i in range(M):
                    if xy[i] == xy[o] and i != o and inf[i] == 1 and random.randint(0, 100) <= tr:
                        susceptible -= 1
                        exposed += 1
                        inf[i] = 2
                        inf_timer[i] = 0
                        # Yes, this implies that some actors will start with counter 0, while others counter 1.
                        # It is not a bug, it is a feature, because we are adding a bit of randomness to
                        # the incubation period (making it 6-7 days instead of 7 days for everyone).
                if inf_timer[o] > rec_period:
                    if random.randint(0, 1) == 0:
                        inf[o] = 0
                        infected -= 1
                        recovered += 1
            else:
                yellow_circles.append(Circle((xy[o][1], xy[o][0]), 0.4, fill=False))
        # Green circle for vaccinated individuals
        elif inf[o] == 0:
            green_circles.append(Circle((xy[o][1], xy[o][0]), 0.4, fill=False))
    # Clear previous circles
    for c in circles:
        c.remove()
    circles.clear()
    # Add new circles in bulk to not cause lag
    if red_circles:
        red_pc = PatchCollection(red_circles, edgecolor='red', facecolor='none')
        ax.add_collection(red_pc)
        circles.append(red_pc)
    if yellow_circles:
        yellow_pc = PatchCollection(yellow_circles, edgecolor='yellow', facecolor='none')
        ax.add_collection(yellow_pc)
        circles.append(yellow_pc)
    if green_circles:
        green_pc = PatchCollection(green_circles, edgecolor='green', facecolor='none')
        ax.add_collection(green_pc)
        circles.append(green_pc)
    if timer == FpD/2:
        timer = 0
        sus_list.append(f"{susceptible: 03}")
        exp_list.append(f"{exposed: 03}")
        inf_list.append(f"{infected: 03}")
        rec_list.append(f"{recovered: 03}")
        vac_list.append(f"{vaccinated: 03}")


def update(frame):
    # Reset grid and remove circles
    grid[:] = 0
    time()
    im.set_data(grid)
    return [im]


# Variable parameters
M = 400   # Number of people
N = 30    # Grid size
FpD = 10  # How many frames is one day. This affects incubation and recovery timeframes, and data printing.
exp_ini = 1     # How many exposed initially
inf_ini = 0     # How many infected initially
rec_ini = 0     # How many recovered initially
vac_ini = 380    # How many vaccinated initially
transmission_rate = 0.9  # Transmission rate, which is 0.9 for measles.

# Fixed parameters from variable parameters
sus_ini = M - vac_ini - rec_ini - inf_ini - exp_ini  # How many susceptible initially
inc_period = FpD * 7  # How long until the disease becomes infectious and harmful
rec_period = FpD * 18  # How long until recovery attempts (50% chance to recover every frame) are made.
tr = transmission_rate*100  # Real transmission rate used, which represents 1 in "tr" chance of contracting it.
sus_list = []
exp_list = []
inf_list = []
rec_list = []
vac_list = []
circles = []
timer = 0
data_counter = 0
susceptible = sus_ini
exposed = exp_ini
infected = inf_ini
recovered = rec_ini
vaccinated = vac_ini


# Create Population
xy = [[random.randint(0, N-1), random.randint(0, N-1)] for _ in range(M)]
inf = [0 if z < vac_ini else 1 for z in range(M)]
infected_starer = random.randint(vac_ini, M)
inf[infected_starer] = 2
inf_timer = {infected_starer: 0}

# Initialize empty grid (all zeros)
grid = np.zeros((N, N))

fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='viridis', vmin=0, vmax=10)


ani = FuncAnimation(fig, update, interval=50)   # updates every 50ms

fig.canvas.new_timer(interval=80000, callbacks=[(stop_animation, [], {})]).start()  # Stop animation after 80000 ms

plt.show()

