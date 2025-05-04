# Vaccination Model: Simulation for the parameter of Beta

import matplotlib.pyplot as plt
import numpy as np
import random as random
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches


# Stop the animation after 5 seconds
def stop_animation():
    global beta_list, xy
    # Stop animation
    ani.event_source.stop()
    print("Animation restarted.")
    # Print list of encounters
    print(beta_list)
    # Print info to SIM0.txt
    with open("SIM0llistes.txt", "a") as f:
        print(beta_list, file=f)
        print("\n ", file=f)
    # Clear list of encounters
    beta_list = []
    # New positions
    xy = [[random.randint(0, N - 1), random.randint(0, N - 1)] for _ in range(M)]
    # Restart Animation
    ani.event_source.start()


# Time loop: Defines new positions and lists others in the same position.
def time():
    b = 0
    for o in range(M):
        # Position Changes
        x_new = xy[o][0]+random.randint(-1, 1)
        y_new = xy[o][1]+random.randint(-1, 1)
        xy[o][0] = max(0, min(N - 1, x_new))
        xy[o][1] = max(0, min(N - 1, y_new))
        grid[xy[o][0], xy[o][1]] += 1  # Increment value at position
        # List matching positions
        if xy.count(xy[o]) > 1:
            b += xy.count(xy[o])-1
    beta_list.append((FpD*b/(M*100)))


# Grid update for the GUI to show properly and delete old positions
def update(frame):
    # Reset grid and remove circles
    grid[:] = 0
    time()
    im.set_data(grid)
    return [im]


# Relevant parameters. Base for measles is 400, 30, 10; while for Covid-19 is 100, 50, 10.
M = 400    # Number of people
N = 30     # Grid size
FpD = 10   # Frames per day. Affects \beta calculation.

beta_list = []

# Create Population
xy = [[random.randint(0, N-1), random.randint(0, N-1)] for _ in range(M)]

# Initialize empty grid (all zeros)
grid = np.zeros((N, N))

fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='viridis', vmin=0, vmax=10)  # Choose color map

ani = FuncAnimation(fig, update, interval=50)  # updates every 50ms

fig.canvas.new_timer(interval=5000, callbacks=[(stop_animation, [], {})]).start()  # Stop animation after 5000 ms

plt.show()

