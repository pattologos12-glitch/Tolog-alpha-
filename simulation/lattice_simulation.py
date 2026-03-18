import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- TOLOG-ALPHA v1.2: VISUAL GRID SYSTEM ---
N = 9
grid_size = (3, 3)
K = 0.8
dt = 0.1
steps = 400

phases = np.random.rand(N) * 2 * np.pi
history_R = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

def update(frame):
    global phases
    # Defekt v kroku 150
    if frame == 150:
        phases[4] += np.pi
        print("CRITICAL: Tolog-Alpha Center Node Defect!")

    # Výpočet synchronizace
    new_phases = phases.copy()
    for i in range(N):
        coupling = np.sum(np.sin(phases - phases[i])) / N
        new_phases[i] += dt * K * coupling
    phases = new_phases

    # Data pro graf
    R = np.abs(np.sum(np.exp(1j * phases)) / N)
    history_R.append(R)

    # Vizualizace mřížky (3x3)
    ax1.clear()
    grid = phases.reshape(grid_size)
    ax1.imshow(np.sin(grid), cmap='viridis', vmin=-1, vmax=1)
    ax1.set_title(f"Tolog-Alpha Grid (Step {frame})")
    for i in range(3):
        for j in range(3):
            ax1.text(j, i, f"{grid[i,j]:.1f}", ha='center', va='center', color='white')

    # Graf stability
    ax2.clear()
    ax2.plot(history_R, color='lime')
    ax2.set_title("Stability Parameter R")
    ax2.set_ylim(0, 1.1)
    if frame > 150:
        ax2.axvline(x=150, color='red', linestyle='--')

ani = animation.FuncAnimation(fig, update, frames=steps, interval=50, repeat=False)
plt.show()